#!/usr/bin/env python3
"""Build exact source/proof hashes for the complete Bernoulli residual branch."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPO = "https://github.com/CocoSgt/riemann-hypothesis-lean"
BASE = REPO + "/blob/" + PIN + "/"
P = "src/Development/AutomorphicArithmetic/AutomorphicVarieties/"
C = "bernoulli_residual_vanishing"
PATHS = {
    "interfaces": P + "LevelCohomology/UnramifiedCocycleIsCoboundaryOfBernoulliUnit.lean",
    "powers": P + "LevelCohomology/ExistsPowDvdSubOfTwoPowDvdSubOne.lean",
    "two": P + "LevelCohomology/TwoPowDvdSubOneOrAddOneOfPowTwoPow.lean",
    "filter": P + "LevelCohomology/SumFilterTwoPowRootsEqZeroOfSumEqZero.lean",
    "partial": P + "LevelCohomology/LxPartial.lean",
    "core": P + "LevelCohomology/LxCore.lean",
    "lemma": P + "LevelCohomology/LemmaX.lean",
    "half": P + "LevelCohomology/PrimitiveTwoPowCharacterOneAddHalfEqNegOne.lean",
    "resmap": P + "LevelCohomology/ExistsResidueMapPadicAlgClIntegers.lean",
    "residual": P + "LevelCohomology/ResidualBernoulliNonvanishing.lean",
    "join": P + "LevelCohomology/ChrInvNeg.lean",
    "coc": P + "PrimitiveFrobeniusFixed/IsAdmissiblePrimeListNil.lean",
    "gal": P + "PrimitiveFrobeniusFixed/GalBasic.lean",
    "cls": P + "CharacterLevelBounds/ClsFacts.lean",
    "norm": P + "GaloisLibrary/SelmerTransport/NormO.lean",
    "b1": P + "GaloisLibrary/BernoulliNumbers/BOneSum.lean",
    "cond": P + "GaloisLibrary/BernoulliNumbers/Condmap.lean",
    "coef": P + "HeightAndVanishing/DirichletPrimeToLPartMulLPowerPart.lean",
    "edat": P + "StickelbergerElements/SamePrimesMulPow.lean",
    "hom": P + "OddResidueBounds/HomKill.lean",
    "clkill": P + "OddResidueBounds/ClKill.lean",
    "field": P + "OddResidueBounds/FixField.lean",
    "dual": P + "GaloisLibrary/KummerTheory/Mk0IdMapCongr.lean",
    "pull": P + "GaloisLibrary/KummerTheory/PullOnto.lean",
    "art": P + "GaloisLibrary/KummerTheory/ArtConj.lean",
    "dict": P + "GaloisLibrary/KummerTheory/ToGalDict.lean",
    "consumer": P + "ModularityArgument/ThresholdArguments/DenseThresholdCases/ConductorAtMapInjectiveCoeff.lean",
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def write(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def main(repo):
    cache = {}
    for key, path in PATHS.items():
        b = (repo / path).read_bytes()
        assert b == subprocess.check_output(["git", "-C", str(repo), "show", PIN + ":" + path]), path
        cache[key] = b

    def anchor(key, decl, start=None, end=None,
               role="exact source interface or reconstructed supplier"):
        b = cache[key]
        lines = b.decode().splitlines()
        if start is None:
            pattern = re.compile(r"^(?:private\s+)?(?:theorem|def|abbrev|structure)\s+" +
                                 re.escape(decl) + r"(?=[\s:(])")
            hits = [i + 1 for i, line in enumerate(lines) if pattern.match(line)]
            assert len(hits) == 1, (key, decl, hits)
            start = hits[0]
        if end is None:
            end = len(lines)
            for i in range(start, len(lines)):
                if re.match(r"^(?:(?:private|noncomputable)\s+)?(?:theorem|def|abbrev|structure|end|section|namespace|variable|instance|attribute|omit|open)\b|^@\[" , lines[i]):
                    end = i
                    break
            while end > start and not lines[end - 1].strip():
                end -= 1
        fragment = b"".join(b.splitlines(keepends=True)[start - 1:end])
        return {
            "path": PATHS[key], "declaration": decl,
            "line_start": start, "line_end": end,
            "sha256": sha(b), "range_sha256": sha(fragment),
            "range_bytes": len(fragment), "first_line": lines[start - 1],
            "url": BASE + PATHS[key] + f"#L{start}-L{end}",
            "role": role, "verified_equal_to_pinned_git_blob": True,
        }

    classical = {
        "schema": "rh-classical-input-registry/1",
        "artifact_version": "0.26", "component": C, "accessed": "2026-11-22",
        "inputs": [
            {
                "id": "BR-CFT", "name": "Finite Hilbert class field and Artin reciprocity",
                "author": "J. S. Milne", "title": "Class Field Theory",
                "version": "4.03", "year": 2020,
                "url": "https://www.jmilne.org/math/CourseNotes/CFT.pdf",
                "theorem_reference": "V Theorems 3.5–3.6 and Example 3.9",
                "printed_pages": [158, 159],
                "web_source_refs": ["turn895130512view0", "turn261223718view0", "turn261223718view1"],
                "accepted_statement": "The maximal finite abelian extension unramified at finite places and split at real places is the Hilbert class field, with Galois group the ordinary ideal class group under Artin.",
                "exact_specialization": "BR4: the locally constant homomorphism z|G_F has finite image inside the original arbitrary field k, hence cuts out an actual finite unramified abelian extension of the same F=Q(mu_N) inside Omega. F is totally complex for N>2. The original map therefore factors through Cl(F); conjugation carries arithmetic Frobenius at a prime to arithmetic Frobenius at the conjugate prime, fixing the inverse orientation in BR.33.",
            },
            {
                "id": "BR-CYC", "name": "Finite cyclotomic Galois identification",
                "author": "J. S. Milne", "title": "Algebraic Number Theory",
                "version": "3.08", "year": 2020,
                "url": "https://www.jmilne.org/math/CourseNotes/ANT.pdf",
                "theorem_reference": "Section 6, basic results on cyclotomic extensions",
                "web_source_refs": ["turn895130512view1", "turn261223718view2"],
                "accepted_statement": "For M>0, Gal(Q(mu_M)/Q) is (Z/M)^× via zeta->zeta^a. Its automorphisms extend to the specified algebraic closure. Q(mu_M) is totally complex for M>2.",
                "exact_specialization": "BR5 realizes a nontrivial character value on the original G_Q, and identifies the mod-l cyclotomic character with the exponent on mu_l when l divides N. BR7 lifts the same CRT unit modulo l*f*2^n in the original Omega; it acts trivially on mu_l but by -1 under both product characters.",
            },
        ],
        "previously_reconstructed_inputs": [
            {
                "claim_id": "OS1", "component": "odd_minus_supplier",
                "used_scope": "Only the principal-ideal identity for theta_(N,r), 1<=r<N, on every ideal of the actual cyclotomic field. Norm/distribution assertions and the later Kolyvagin system are not used.",
                "inherited_classical_inputs": ["OS-CYC", "OS-CHEB", "OS-HCF"],
                "new_transfer": "BR4 extends the theta relation to arbitrary positive a coprime to N, identifies twice the Eone group-ring element with -sigma_a^-1 theta_a, and divides by 2 only after mapping to the actual odd-characteristic k.",
            }
        ],
        "foundational_background": [
            "Finite group orders, elementary valuations and ideal factorization in a DVR",
            "The ultrametric norm on the specified algebraic closure of Q_l and integrality of a module-finite algebra",
            "Compactness of profinite Galois groups and the finite-image consequence of a locally constant function",
            "The Chinese remainder theorem, finite geometric sums and Frobenius in characteristic l",
        ],
        "not_assumed": [
            "LemmaX, CorX, or residual Bernoulli-unit vanishing",
            "Any general Stickelberger ideal-class annihilation theorem",
            "A prescribed Bernoulli-unit or nonvanishing theorem",
            "An Iwasawa main theorem, Kato theorem, automorphy or rigidity",
            "Finiteness or algebraic closedness of the original k",
            "Surjectivity of red:O->k",
            "A prime-to-l order for Gal(Q(mu_N)/Q)",
        ],
    }
    write("classical_inputs.json", classical)

    specs = [
        ("BR1", "Dyadic generation and finite Frobenius character-sum projection", [], [], [
            anchor("powers", "UpperTheory.exists_pow_dvd_sub_of_two_pow_dvd_sub_one",
                   role="needed dyadic-generation specialization; proved through exact order and subgroup size"),
            anchor("filter", "UpperTheory.sum_filter_two_pow_roots_eq_zero_of_sum_eq_zero",
                   role="needed n>=e projection; the smaller averaging range 2^(n-e) is proved directly"),
            anchor("two", "UpperTheory.two_pow_dvd_sub_one_or_add_one_of_pow_two_pow",
                   role="source elementary dyadic route replaced by the explicit <5> argument at n=m+e"),
            anchor("core", "pm_of_pow", role="literal needed character-kernel conclusion for m>=e>=2"),
        ]),
        ("BR2", "Integral partial Bernoulli sums without division by the odd conductor", [], [], [
            anchor("partial", "shift_sum"),
            anchor("partial", "lx_partial"),
            anchor("lemma", "UpperTheory.V.X.prodX_nat"),
            anchor("lemma", "UpperTheory.V.X.genB_prodX"),
            anchor("b1", "UpperTheory.V.Bern.b_one"),
            anchor("interfaces", "prodX"),
        ]),
        ("BR3", "Literal LemmaX at the prescribed power-of-two conductor", ["BR1", "BR2"], [], [
            anchor("resmap", "UpperTheory.exists_residue_map_padicAlgCl_integers"),
            anchor("half", "UpperTheory.primitive_two_pow_character_one_add_half_eq_neg_one"),
            anchor("core", "lx_core"),
            anchor("lemma", "UpperTheory.V.X.lemmaX"),
            anchor("interfaces", "XData"),
            anchor("interfaces", "LemmaX"),
        ]),
        ("BR4", "Original tame-index unramified condition and Jacobi annihilation", ["OS1"], ["BR-CFT", "BR-CYC"], [
            anchor("interfaces", "UnrEv"),
            anchor("residual", "zero_of_unr"),
            anchor("coc", "IsCoc"),
            anchor("dual", "XDual"),
            anchor("pull", "UpperTheory.V.Kum.pullOnto",
                   role="needed N'=1, totally-complex, additive-k specialization reconstructed by actual finite class-field descent"),
            anchor("dict", "UpperTheory.V.Kum.toGalDict"),
            anchor("art", "UpperTheory.V.Kum.artConj"),
            anchor("edat", "yCl"), anchor("edat", "jv"), anchor("edat", "Eone"),
            anchor("coc", "th"), anchor("coc", "IsX"),
            anchor("clkill", "UpperTheory.V.Odd.clKill",
                   role="stronger source integral interface is NOT claimed proved; BR4 derives the sufficient doubled relation from OS1"),
            anchor("hom", "UpperTheory.V.Odd.homKill",
                   role="only the E=Q, N'=1, R=X=k, char(k)=l odd specialization is claimed, with no unmatched input"),
            anchor("field", "UpperTheory.V.Odd.fixField"),
        ]),
        ("BR5", "The exact nonzero residual Bernoulli scalar on original coefficients", [], ["BR-CYC"], [
            anchor("coef", "Coef"),
            anchor("residual", "unit_of_norm"),
            anchor("residual", "unit_of_red"),
            anchor("residual", "red_chi"),
            anchor("residual", "red_ne_one"),
            anchor("residual", "sum_units"),
            anchor("residual", "sum_icc"),
            anchor("residual", "sum_eone"),
            anchor("residual", "exists_odd"),
            anchor("norm", "UpperTheory.V.Base.normO"),
            anchor("interfaces", "redChar"),
            anchor("gal", "UpperTheory.V.ML.galBasic"),
            anchor("cls", "UpperTheory.V.Chr.clsFacts"),
            anchor("b1", "UpperTheory.V.Bern.b_one"),
        ]),
        ("BR6", "Full residual unramified Bernoulli-unit cocycle theorem", ["BR4", "BR5"], [], [
            anchor("residual", "UpperTheory.V.X.residual_bernoulli_nonvanishing"),
            anchor("interfaces", "UnramifiedCocycleIsCoboundaryOfBernoulliUnit"),
            anchor("interfaces", "UnrEv"),
            anchor("interfaces", "redChar"),
            anchor("coc", "IsCoc"),
            anchor("gal", "UpperTheory.V.ML.galBasic"),
        ]),
        ("BR7", "Complete CorX on both original residual characters", ["BR3", "BR6"], ["BR-CYC"], [
            anchor("join", "prodX_map"), anchor("join", "prodX_inv"),
            anchor("join", "chr_inv_neg"), anchor("join", "xd_inv"),
            anchor("join", "xd_map"), anchor("join", "xd_ne_two"),
            anchor("join", "xi_pow"), anchor("join", "xd_ord"),
            anchor("join", "xd_neg", role="replaced by the more explicit half-period element already proved in BR3"),
            anchor("join", "xd_gal"),
            anchor("join", "red_chi"),
            anchor("join", "main"), anchor("join", "UpperTheory.V.X.corX"),
            anchor("cond", "UpperTheory.V.Bern.b_condmap"),
            anchor("interfaces", "XData"), anchor("interfaces", "CorX"),
            anchor("consumer", "UpperTheory.V.Th.sp4Main_alt",
                   role="downstream conditional paired-count consumer; no other hypotheses are asserted supplied here"),
        ]),
    ]
    raw = (HERE / "main.tex").read_bytes()
    lines = raw.splitlines(keepends=True)
    claims = []
    for cid, title, deps, cin, sources in specs:
        starts = [i for i, line in enumerate(lines)
                  if re.search(rb"\\begin\{(?:proposition|theorem)\}\[" + cid.encode() + b":", line)]
        assert len(starts) == 1, cid
        a = starts[0]
        b = next(i for i in range(a, len(lines)) if lines[i].strip() == rb"\end{proof}")
        fragment = b"".join(lines[a:b + 1])
        loc = {"file": C + "/main.tex", "line_start": a + 1,
               "line_end": b + 1, "sha256": sha(fragment), "bytes": len(fragment)}
        claims.append({
            "id": cid, "title": title,
            "status": "Complete human proof in the stated scope, relative to the explicitly matched classical inputs and previously proved OS1.",
            "depends_on": deps, "mathematical_dependencies": deps,
            "classical_inputs": cin, "remaining_inputs": [],
            "remaining_bespoke_inputs": [], "component_ledger": C + "/provenance.json",
            "proof_location": loc, "human_proof": loc, "sources": sources,
        })
    files = [
        {"path": PATHS[key], "sha256": sha(b), "bytes": len(b),
         "lines": len(b.splitlines()), "url": BASE + PATHS[key],
         "verified_equal_to_pinned_git_blob": True}
        for key, b in cache.items()
    ]
    validation = {
        "main_tex_sha256": sha(raw), "claim_count": len(claims),
        "source_links": sum(len(c["sources"]) for c in claims),
        "source_files": len(files), "all_sources_equal_pinned_git_blobs": True,
        "all_source_and_proof_range_hashes_recorded": True,
        "kernel_replay": False, "full_lean_build": False, "pdf_generated": False,
    }
    not_supplied = [
        "Unrestricted integral clKill or arbitrary-coefficient homKill",
        "SymplecticFourImageDense, NumberSp4Alt, RigiditySymplecticFour",
        "The other hypotheses of the CountII/CountIII consumer",
        "CountI, CountV or the full PointHV interface",
        "Actual global family, gap, LinkN, theta/type/rank, metric or spectral suppliers",
        "An unconditional human-readable RH or Dirichlet GRH proof",
    ]
    boundary = {
        "previously_proved_claims": ["OS1"],
        "bespoke_inputs": [], "classical_inputs": ["BR-CFT", "BR-CYC"],
        "inherited_classical_inputs_via_OS1": ["OS-CYC", "OS-CHEB", "OS-HCF"],
        "not_supplied": not_supplied,
    }
    write("provenance.json", {
        "schema": "rh-human-reconstruction-provenance/1",
        "artifact_version": "0.26", "date": "2026-11-22",
        "repository": REPO, "commit": PIN, "component": C,
        "main_tex_sha256": sha(raw),
        "scope": "Full literal LemmaX, residual Bernoulli-unit cocycle theorem and CorX, at prescribed dyadic conductor and on the original Omega, O, red and arbitrary k, with both character choices and actual tame relative-index conditions.",
        "claims": claims, "source_files": sorted(files, key=lambda f: f["path"]),
        "mathematical_dependency_graph": {c["id"]: c["depends_on"] for c in claims},
        "classical_input_registry": C + "/classical_inputs.json",
        "component_input_boundary": boundary, "validation": validation,
    })
    write("source_hashes.json", {"commit": PIN, "files": sorted(files, key=lambda f: f["path"])})
    write("verification.json", validation)
    write("closure.json", {
        "artifact_version": "0.26", "component": C, "commit": PIN,
        "main_tex_sha256": sha(raw), "claims": [c["id"] for c in claims],
        "closed_bespoke_interfaces": [
            {"interface": "UpperTheory.V.X.LemmaX", "supplied_by": "BR3",
             "source": anchor("interfaces", "LemmaX"),
             "scope": "All original XData, exact f*4^v2(l^d-1)<=2^n threshold, original specified l-adic algebraic closure; no later conductor enlargement."},
            {"interface": "UpperTheory.V.X.UnramifiedCocycleIsCoboundaryOfBernoulliUnit",
             "supplied_by": "BR6",
             "source": anchor("interfaces", "UnramifiedCocycleIsCoboundaryOfBernoulliUnit"),
             "scope": "All original Omega, odd l, finite DVR Coef.O, arbitrary char-l field k, arbitrary unital red, nontrivial prime-to-l chi distinct residually from cyclotomic, specified-level inverse-character Bernoulli unit, all locally constant cocycles and exactly UnrEv."},
            {"interface": "UpperTheory.V.X.CorX", "supplied_by": "BR7",
             "source": anchor("interfaces", "CorX"),
             "scope": "Both original redChar(prodX phi xi) and its inverse, all original XData and residue-field/tame-index quantifiers."},
        ],
        "remaining_bespoke_inputs": [],
        "previously_proved_inputs": ["OS1"],
        "classical_inputs": ["BR-CFT", "BR-CYC"],
        "safe_to_retire_in_stated_scope": ["DA25-HV-05"],
        "partial_target_updates": {
            "DA25-HV-03": {
                "newly_supplied_inputs": {"UpperTheory.V.X.CorX": "BR7"},
                "remaining_human_scope": "Retain the other actual hypotheses and the paired-count construction unless supplied by separately reviewed v0.26 components.",
            }
        },
        "exact_binding_notes": [
            "The original XData inequality is used at the prescribed n: e=v2(l^d-1), m=n-e, s=f*2^e<=2^m.",
            "No division by f is used in the integral partial Bernoulli sum, so l may divide f.",
            "The Frobenius projection is proved by finite dyadic generation and a geometric sum; the final contradiction is exactly 0=-2.",
            "The auxiliary residue field in BR3 tests a norm only; it never replaces the arbitrary k in the outgoing residual theorem.",
            "UnrEv has index [I_A intersect ker gamma : H_A intersect I_A intersect ker gamma], with no assumption H_A<=I_A.",
            "Locally constant cocycles have finite image on the actual closed G_F, allowing finite class-field theory for arbitrary k.",
            "Inertia for the actual F inside Omega is the original inertia intersected with G_F.",
            "The Artin inverse-conjugation convention agrees with OS1 and with chi^-1 in the Bernoulli scalar.",
            "The arbitrary positive odd a in Eone is handled even when a>=N.",
            "Only twice the integral Eone relation is needed; 2 is canceled after mapping into odd-characteristic k.",
            "The original nonsurjective red map has kernel equal to the maximal ideal of the original O.",
            "The global cocycle is killed using an abelian quotient and one gamma(h)-1 inverse, not division by its potentially l-divisible order.",
            "Both inverse characters use the same CRT element fixing mu_l and evaluating to -1.",
        ],
        "does_not_close": not_supplied,
    })

    parent = HERE.parent
    previous_files = [
        "odd_minus_supplier/main.tex", "odd_minus_supplier/provenance.json",
        "odd_minus_supplier/report.md", "odd_minus_supplier/closure.json",
    ]
    previous = json.loads((parent / "odd_minus_supplier/provenance.json").read_text())
    os1 = next(c for c in previous["claims"] if c["id"] == "OS1")
    loc = os1["human_proof"]
    b = (parent / loc["path"]).read_bytes()
    fragment = b"".join(b.splitlines(keepends=True)[loc["line_start"] - 1:loc["line_end"]])
    assert sha(fragment) == loc["range_sha256"], "OS1 human proof bytes changed"
    write("input_manifest.json", {
        "artifact_version": "0.26", "component": C,
        "pinned_source_commit": PIN,
        "previous_human_inputs": [
            {"claim_id": "OS1", "human_proof": loc,
             "verified_range_hash": sha(fragment),
             "used_scope": "The principal-ideal relation only, with its inherited finite classical inputs."}
        ],
        "files": [
            {"path": path, "bytes": len((parent / path).read_bytes()),
             "sha256": sha((parent / path).read_bytes())}
            for path in previous_files
        ],
        "no_older_file_modified_by_component": True,
    })
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=HERE.parent.parent / "lean-source")
    main(parser.parse_args().repo.resolve())
