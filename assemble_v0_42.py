#!/usr/bin/env python3
"""Assemble the current reader's edition and preserve the cumulative history."""
from pathlib import Path
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent
CFG = json.loads((ROOT / "increment_v0_42.json").read_text())
ST = json.loads((ROOT / "integration_stats_v0_42.json").read_text())
REG = json.loads((ROOT / "dependency_audit_v0_42/remaining_leaf_register.json").read_text())
COV = json.loads((ROOT / "dependency_audit_v0_42/route_coverage.json").read_text())
WEIGHT = "weight_representation_v42" in CFG["components"]
SPEC = "specialization_map_v42" in CFG["components"]
ARITH = "arithmetic_specialization_v42" in CFG["components"]

def mono(m):
    b = re.sub(r"(?<=[a-z])(?=[A-Z])", lambda _: r"\allowbreak ", m[1])
    b = re.sub(r"\.(?!\\allowbreak)", lambda _: r".\allowbreak ", b)
    b = re.sub(r"([/:])(?!\\allowbreak)", lambda m: m[1] + r"\allowbreak ", b)
    b = re.sub(r"\\_(?!\\allowbreak)", lambda _: r"\_\allowbreak ", b)
    return r"\texttt{" + b + "}"

def wraps(t):
    t = re.sub(r"\\texttt\{([^{}]*)\}", mono, t)
    t = re.sub(r"\\_(?!\\allowbreak)", lambda _: r"\_\allowbreak ", t)
    return re.sub(r",(?=[A-Za-z])", lambda _: r",\allowbreak{} ", t)

def esc(s):
    table = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
             "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
             "^": r"\textasciicircum{}", "≤": r"$\le$", "≥": r"$\ge$",
             "→": r"$\to$", "ℓ": r"$\ell$", "𝒞": r"$\mathcal C$"}
    return "".join(table.get(c, c) for c in s)

audit_head = r"""\section{Current dependency audit: ordinary structure, rigidity, and quantitative reductions}
\label{sec:dependency-audit-v42}

\subsection{Current status and reading order}

This version gives a complete conditional terminal argument and completes
the roadmap's finite-level, ordinary-structure and base-change milestone.
It also proves the original classical control and local Hecke-algebra
theorems on their stated arithmetic inputs. Both previously unresolved
theorem-matching obligations are now reconstructed: the full original
\texttt{AdVanishK} and the full original \texttt{HostRigid\_s}.
The finite-field row calculations and the global quantitative reductions
give further proved inputs to the selected route.

The underlying Alpoge--Claude Lean proof is accepted as fully checked and
correct. This manuscript remains a \textbf{partial human reconstruction}:
the common arithmetic and geometric objects, their compatible arithmetic
specializations, and the five original global quantitative producers are
not all reconstructed. No Lean build or kernel replay is claimed.

There are @NEW@ new and @TOTAL@ cumulative proof claims. The selected graph
retains 121 nodes and 161 logical edges. Its open register has @OPEN@
whole obligations, @C@ of class C and @B@ of class B, with no remaining
class-D matching obligation. Of these, @SHARED@ are shared by RH and
Dirichlet GRH and @GRH@ are additional for Dirichlet GRH; none is RH-only.
The count is an inventory of scopes, not a percentage of completion.
Every predecessor claim, source array and dependency edge is preserved.

Read CMP1--CMP6 first for the complete conditional final deduction.
The ordinary entrance is FNL, OST, OCT and OHA; the two rigidity chapters
are ADK and HSR. RRT and GQT supply the finite row arguments and sufficient
quantitative replacements. The source pin and exact claim-to-source
records are in the accompanying provenance ledger. The separate file
\texttt{RH\_new\_proofs\_v0\_42.tex} contains this audit and only the
current increment. Historical chapters below retain their original
hypotheses; this audit governs their older frontier descriptions.

\subsection{The completed ordinary entrance}

FNL1--FNL16 prove the actual finite adelic factorization in its required
order, and all eighteen original \texttt{HSet.Ax} fields. They verify the
local split sections, auxiliary congruence condition, Iwahori topology,
level joins, original Artin maps and inverse-Frobenius density on the
same objects used by the ordinary theory.

OST1--OST28 construct one factorial-limit projector onto the actual
ordinary module. They prove its exact value filtration, finite freeness,
invertibility of every positive-monoid operator, and base change by the
original coefficientwise map for every allowed local map of complete
Noetherian local rings. Neither nilpotents nor nonflat local maps are
excluded. The local matrix and product-group axioms are proved before
the theorem is installed on each original level.

OCT1--OCT19 prove the original control theorem by identifying an integral
ordinary classical lattice with the actual ordinary module. The proof
retains the original coefficient domain, injective embedding and all ten
\texttt{WtRep} fields. The zeroth-coordinate control map, normalized
positive operators, depth comparisons and finite away sums are checked
on the same functions. OHA1--OHA12 prove spherical commutativity and the
full original \texttt{hiComm}/\texttt{hiAlg}: the literal residual part
is the appropriate idempotent summand of the finite commuting operator
algebra, its Hecke algebra is finite complete local with the prescribed
residue field, and the positive generators are units in that algebra.

@WEIGHT@

The full integral type, arithmetic specialization and separating fibers,
the four original Hida endpoints and all-level automorphy on one ideal
still have to be supplied. Both original rank-four Links, the fixed
complex embedding, residue characteristic three and one common
coefficient threshold remain in scope. The selected Raw implication
proved in the predecessor is reused, not reopened.

\subsection{Two whole matching obligations now closed}

ADK1--ADK6 prove the exact application of Thorne's adjoint
Bloch--Kato vanishing theorem. The comparison includes normalized
Satake parameters, the infinite-place algebraicity dictionary,
conjugate self-duality, finite coefficient descent, irreducibility on
the full infinite cyclotomic kernel, and the literal local finite
conditions. It uses the full matrix adjoint, including the scalar line
and negative-transpose complex-conjugation action. It holds throughout
the source contract, in every rank at least two and every allowed prime.

HSR1--HSR9 prove the original host-rigidity implication. The dyadic
conductor gives an actual separating local element. An allowed
dual-number deformation yields a Bloch--Kato cocycle by the written
ordinary crystalline argument and the actual local comparison maps.
The original automorphic representation is twisted by
$\epsilon^{-1}$, its pairing is the actual antidiagonal matrix $J$,
and its full adjoint is the representation to which ADK6 applies.
Surjectivity of the original quotient map gives one global primitive
with the required sign. No new host-existence or automorphy theorem is
inferred, and the distinct \texttt{RIG\_II} producer remains open.

\subsection{The conditional main theorem and quantitative progress}

CMP1--CMP6 give the final derivation from two precisely stated common
arithmetic input contracts. Exact character orthogonality, including
ramified prime readings, identifies the centered prime sum. Fourier
averaging precedes estimation. The arithmetic comparison gives the
one-sided square-root bound, and the fully written pole argument
excludes zeros to its right. Functional equations and the elementary
imprimitive Euler factors finish RH and unrestricted Dirichlet GRH.
The conclusion remains conditional until the two input contracts are
produced. CMP1, CMP3, CMP4 and CMP5 reorganize inherited proofs; they
are not counted as new arithmetic input theorems.

GQT1--GQT7 show that only three counting tests are needed for the
retained-row defect, and give polynomial error conditions sufficient
for the final spectral consumer. All common spaces, metrics, measures,
integral lattices and normalization factors remain fixed as required.
The exact original stronger spectral producer is not claimed.

RRT1--RRT16 prove positivity and normalization of the actual finite
weights, probability transfer, squarefree and divisor bounds, the
$7/8$ invariant-subset estimate, an eventual long-cycle estimate and
the full original root-to-twist collision estimate with its constants.
They also prove the finite tensor identity and the actual repeated-label
enumeration on supplied multiplicity identities. Four of the five
displayed terms of $W_g$ now have local producers. The remaining local
inputs are two exact character laws (with the original label matching)
and the root-injectivity collision estimate. The global row identities,
adelic inflation comparison and three arithmetic counts remain to be
constructed. Thus \texttt{GLOBAL\_RETAINED\_DEFECT} is still open.

\subsection{The remaining route}

The next large arithmetic endpoint is one same-ideal Hida/support
package on both original rank-four Links. A second endpoint is one
compatible geometric and local family carrying all required readings,
tests, point identities, lattices and base rows. Separate witnesses
for those properties do not suffice. The one-character, congruence,
host-counting and additional Dirichlet-GRH branches retain their original
quantifiers. The denominator, retained-defect, period/height, local-gain
and spectral estimates must all be installed on that common family.

Classes A, B, C and D retain the roadmap's meaning: checked published
application, independent elementary/moderate reconstruction, substantial
reconstruction, and unresolved source matching respectively.
Classification and completion are separate. The two D questions have
been resolved by proofs; this does not reclassify the remaining C tasks
as easy. All 245 historical compound targets remain traceable.

\subsection{Every remaining selected obligation}

The following contracts retain the exact selected outputs. Progress
inside a compound contract is recorded immediately after its statement.
Completed subtheorems are available inputs; a compound contract remains
open until all its actual input producers and compatibility conditions
have been reconstructed.
"""
weight_text = (r"The additional weight-representation chapter constructs the original "
               r"algebraic representation's integral lattice and all ten \texttt{WtRep} "
               r"assertion fields, with the specified complex embedding retained. "
               r"It supplies the algebraic representation required by control; "
               r"arithmetic specialization and separating fibers remain separate."
               if WEIGHT else
               r"The algebraic \texttt{WtRep} producer remains an explicit input to the "
               r"completed control theorem; it is not inferred from control itself.")
if SPEC:
    weight_text += (r"\par SMP1--SMP10 prove the full original \texttt{Sp.absSpec}: "
                    r"one map on all ambient functions, fixed before every level, depth, "
                    r"basis and operator. Finite modules of untwisted values prove both "
                    r"eigenvalue-integrality assertions. The full finite away-sum clause "
                    r"uses only its original fixed-space hypothesis, without requiring "
                    r"its coefficient-valued image to be ordinary.")
if ARITH:
    weight_text += (r"\par The arithmetic-specialization chapter installs this same map "
                    r"in the original \texttt{SpecIntIff.spec}, with the actual "
                    r"coefficient point, finite-part character, prescribed complex "
                    r"embedding and all original \texttt{IsSpec} fields. Arithmetic "
                    r"nonvanishing and separation of fibers remain separate producers.")
    audit_head=audit_head.replace("The full integral type, arithmetic specialization and separating fibers,",
                                  "The full integral type and separating arithmetic fibers,")
replacements = {"@NEW@": ST["new_claims"], "@TOTAL@": ST["cumulative_claims"],
                "@OPEN@": ST["open_count"], "@C@": ST["open_categories"].get("C",0),
                "@B@": ST["open_categories"].get("B",0), "@SHARED@": ST["shared_open"],
                "@GRH@": ST["extra_grh_open"], "@WEIGHT@": weight_text}
for a,b in replacements.items(): audit_head = audit_head.replace(a,str(b))

# Reuse the precise existing contract statements, remove only discharged entries,
# and supersede their historical internal progress descriptions explicitly.
old_audit = (ROOT / "dependency_audit_v0_41/main.tex").read_text()
blocks = re.split(r"(?=^\\paragraph\{\d+\.)", old_audit, flags=re.M)[1:]
by_id = {}
for block in blocks:
    heading = block.splitlines()[0].replace(r"\allowbreak{}", "").replace(r"\_", "_")
    key = re.search(r"\\paragraph\{\d+\. (\S+) —", heading)[1]
    by_id[key] = block
body = []
for i,record in enumerate(REG["records"],1):
    block = re.sub(r"^\\paragraph\{\d+\.", lambda _: r"\paragraph{"+str(i)+".", by_id[record["id"]],count=1)
    if record["id"] == "COUNT_II_SUPPORT":
        a = block.index("The current producers are")
        b = block.index("The selected Raw patching", a)
        block = block[:a] + (
            "FNL, OST, OCT and OHA now supply the full original finite-level and HSet axioms, "
            "ordinary projector, freeness, base change, control on its weight representation, "
            "and local Hecke algebra. " +
            ("The algebraic weight representation is also constructed in the new weight chapter. " if WEIGHT else "") +
            "The remaining arithmetic producers are the full original integral TypeForAlt; " +
            ("separating automorphic arithmetic fibers; the four Hida " if ARITH else
             "actual arithmetic specialization and separating automorphic fibers; the four Hida ") +
            "endpoints PointTheoremBaseObject, ArithmeticPointDecomposition, IrrArithPointsAutomorphicAway "
            "and TwistOk on this same ideal; and all-level same-ideal LevelAlt, TWAut and HasAut "
            "on both original Links. "
        ) + block[b:]
    progress = CFG.get("selected_node_progress",{}).get(record["id"])
    if progress:
        block += "\n\\emph{Current subfrontier.} " + esc(progress["remaining"]) + "\n\n"
    body.append(block)
audit = wraps(audit_head + "\n".join(body))
(ROOT / "dependency_audit_v0_42/main.tex").write_text(audit)

source = (ROOT / "RH_readable_reconstruction_v0_41.tex").read_text()
preamble = source[:source.index(r"\begin{document}")]
preamble = preamble.replace("working version 0.41", "working version 0.42").replace("Working version 0.41", "Working version 0.42")
main = source.replace("working version 0.41", "working version 0.42").replace("Working version 0.41", "Working version 0.42")
main = main.replace("Neat levels, ordinary weights, and exact local tests", "Ordinary structure, rigidity, and quantitative reductions",1)
main = main.replace("A refined completion audit with 87 new proof claims", f"A completion audit with {ST['new_claims']} new proof claims",1)
main = main.replace("22 November 2026", "23 November 2026",1)
a=main.index(r"\textbf{What version 0.41 achieves.}"); b=main.index(r"\end{minipage}",a)
front = r"""\textbf{What version 0.42 achieves.}
The complete conditional main deduction is written in one place.
The original finite-level, ordinary-freeness and base-change theorems
are proved, followed by classical control and the local Hecke algebra.
The full adjoint-vanishing match and original host rigidity are now
reconstructed. Finite row estimates and sufficient quantitative
simplifications are proved on their exact inputs.

There are @NEW@ new and @TOTAL@ cumulative claims. The selected
whole-obligation register has @OPEN@ remaining entries: @C@ C and @B@ B.
The same-ideal arithmetic inputs, common geometric/local construction,
and global estimate producers remain. This is a
\textbf{partial human reconstruction}, with the assumed-correct formal
proof unchanged. The current audit governs historical frontier notes.
"""
for x,y in replacements.items():front=front.replace(x,str(y))
main=main[:a]+front+main[b:]
marker=re.search(r"^\\section\{[^\n]+",old_audit,re.M)[0]
historical = r"""\paragraph{Historical version-0.41 audit.}
The following checkpoint is preserved for provenance. The current
version-0.42 audit in Section~\ref{sec:dependency-audit-v42} supersedes
its frontier descriptions. Conditional historical proofs retain their
printed hypotheses, including hypotheses now supplied by later chapters.

"""
chapters = wraps("\n\n".join((ROOT/c/"main.tex").read_text() for c in CFG["components"]))
insert = audit + "\n\\clearpage\n" + chapters + "\n\\clearpage\n" + historical
assert main.count(marker)==1
main=main.replace(marker,insert+marker,1)
a=main.index(r"\section{The arithmetic still to be written out}");b=main.index(r"\section{Claim ledger and reading order}",a)
remaining = r"""\section{The arithmetic still to be written out}\label{sec:remaining}
Section~\ref{sec:dependency-audit-v42} is the complete current register.
The ordinary-structure, base-change, control and Hecke-algebra arguments
are now available; ADK and HSR close the two former matching questions.
The following are the remaining large input-producing tasks.
\begin{enumerate}
"""
for t in CFG["remaining_major_inputs"]:remaining+=r"\item "+esc(t)+"\n"
remaining+=r"""\end{enumerate}
The conditional main theorem identifies where each input is used.
The optional AQ route remains optional. Historical RF16 remains governed
by DEX11. No formal-source correctness question is reopened.

"""
main=main[:a]+wraps(remaining)+main[b:]
a=main.index("Start with the version-0.41 audit in",main.index(r"\section{Claim ledger and reading order}"))
b=main.index("including the preserved",a)
b=main.index("RF16 correction.",b)+len("RF16 correction.")
main=main[:a]+r"""Start with the version-0.42 audit in
Section~\ref{sec:dependency-audit-v42} and CMP1--CMP6 for the final
conditional argument. Read the ordinary entrance FNL/OST/OCT/OHA,
the adjoint and host-rigidity chapters ADK/HSR, and the quantitative
chapters RRT/GQT according to the input being reconstructed. Their
explicit references connect to inherited NTL/OTW, CIP/CAP, RX/BX and
the selected Raw support proof. The exact current source and proof
ranges are recorded in the version-0.42 provenance ledger.
All historical chapters remain available, including the preserved
RF16 correction."""+main[b:]
(ROOT / "RH_readable_reconstruction_v0_42.tex").write_text(main)

new_title = r"""\begin{document}
\begin{center}
{\LARGE\bfseries RH and Dirichlet GRH: new reconstruction chapters}\\[7pt]
{\large Version 0.42 --- 23 November 2026}\\[5pt]
{\large Ordinary structure, rigidity, and quantitative reductions}
\end{center}
\textbf{Scope.} This reader's edition contains the current audit and
the new chapters only. It is a partial reconstruction, not a completed
human proof of RH or GRH. References to earlier named claims refer to
the complete cumulative manuscript and the preserved component files
in the accompanying archive. The underlying pinned formal proof is
accepted as correct. The exact current boundary is stated below.
\setcounter{tocdepth}{1}
\tableofcontents
\clearpage
\begingroup\emergencystretch=3em
"""
increment=preamble+new_title+audit+"\n\\clearpage\n"+chapters+"\n\\endgroup\n\\end{document}\n"
(ROOT / "RH_new_proofs_v0_42.tex").write_text(increment)

txt=["RH AND DIRICHLET GRH — DEPENDENCY AUDIT v0.42", "23 November 2026", "",
     CFG["status"], "", "SOURCE PIN", CFG["source_commit"], "",
     "INVENTORY", f"New claims: {ST['new_claims']}; cumulative claims: {ST['cumulative_claims']}.",
     f"Selected graph: 121 nodes, 161 logical edges. Open whole obligations: {ST['open_count']} = {ST['open_categories'].get('C',0)} C + {ST['open_categories'].get('B',0)} B.",
     f"Shared by RH and GRH: {ST['shared_open']}; additional Dirichlet-GRH-only: {ST['extra_grh_open']}; RH-only: zero.",
     "These are scopes, not a completion percentage. D means unresolved source matching, not a claim about formal correctness. Both former D questions are now resolved.", "",
     "WHOLE OBLIGATIONS CLOSED IN THIS VERSION"]
for k,v in CFG["closed_selected_leaves"].items():txt += [k, v["conclusion"], "Proof: "+", ".join(v["claims"]), v["method"], ""]
txt += ["NEW PROVED RESULTS"]
for i,t in enumerate(CFG["local_conclusions"],1):txt += [f"{i}. {t}", ""]
txt += ["COMPLETE CURRENT OPEN-OBLIGATION REGISTER", "The exact original contract is retained; current progress notes supersede its historical internal frontier wording.", ""]
for i,r in enumerate(REG["records"],1):
    txt += [f"{i:02d}. {r['id']} — {r['category']} — {r['title']}", "Contract: "+r["contract"]]
    if r.get("bindings"):txt += ["Shared-object and choice-order bindings: "+"; ".join(r["bindings"])]
    if r.get("version_0_42_progress"):
        p=r["version_0_42_progress"]
        txt += ["New completed inputs: "+", ".join(p["completed"]),"Current remaining subfrontier: "+p["remaining"]]
    for e in r.get("evidence",[]):
        txt += [f"Source: {e.get('declaration','')} — {e.get('url',e.get('path',''))}"]
    txt.append("")
txt += ["NEXT LARGE ENDPOINTS"]+CFG["remaining_major_inputs"]+["", "VALIDATION SCOPE", "See validation_v0_42.json, tex_validation.json, and the hash-bound independent reviews. TeX draft compilation checks syntax and references. No PDF visual review or Lean replay is claimed."]
(ROOT / "RH_dependency_audit_v0_42.txt").write_text("\n".join(txt)+"\n")

readme = "\n".join([
"# RH and Dirichlet-GRH reconstruction — v0.42", "", "23 November 2026", "", CFG["status"], "",
"## Reading order", "",
"1. `RH_reconstruction_progress_v0_42.txt`: changes, roadmap milestones, mathematical ideas and next endpoints.",
"2. `RH_new_proofs_v0_42.tex`: current audit and all new proof chapters, without the historical accumulation.",
"3. `RH_readable_reconstruction_v0_42.tex`: cumulative manuscript, preserving all earlier proof chapters.",
"4. `RH_dependency_audit_v0_42.txt`: complete current selected obligation register, source references and compatibility constraints.",
"5. `continuation_checkpoint.json`, `next_source_targets.json`, `provenance.json` and `dependency_audit_v0_42/`: machine-readable continuation and exact contracts.", "",
"## Current boundary", "",
f"{ST['new_claims']} new claims; {ST['cumulative_claims']} cumulative claims. The selected graph remains 121 nodes and 161 edges. {ST['open_count']} whole obligations remain: {ST['open_categories'].get('C',0)} C and {ST['open_categories'].get('B',0)} B. Two former D matching obligations are closed, with no remaining D entry. This is not a percentage of proof completion.", "",
"Both rank-four Links, prime 3, fixed complex embeddings, original ideals, coefficient fields, actions, lattices, metrics, measures and uniform thresholds remain in scope. GRH means the unrestricted Dirichlet-L-function generalization in the source.", "",
"## Proof chapters", ""] + ["- `"+c+"/main.tex`" for c in CFG["components"]] + ["",
"Component provenance files give exact human proof ranges and pinned source ranges. The current mathematical dependency DAG is not represented as a Lean transitive dependency audit. The new `source_snapshot_v0_42/` contains the pinned source files cited by the increment; earlier snapshots are preserved.", "",
"## Verification and history", "",
"`validation_v0_42.json` records preservation, hashes, selected-graph and mathematical-DAG checks. `tex_validation.json` records draft-mode compilation and any limitations. Hash-bound mathematical reviews are in `reviews_v0_42/` and the component folders. No Lean build, kernel replay, PDF generation or visual PDF review is claimed.", "",
"All previous named files are preserved. Mutable root files from v0.41 are preserved byte-for-byte in `history/version_0_41/`. The current audit supersedes historical frontier prose; historical conditional theorems retain their hypotheses. `SHA256SUMS` covers the distributed files.", "",
"Source pin: `"+CFG["source_commit"]+"`.", "",
"The integration, assembly, validation and packaging scripts are included for reproducibility. Re-running source checks requires the pinned source checkout at the path documented by those scripts.", ""])
(ROOT / "README.md").write_text(readme)
print(json.dumps({"main_bytes":len(main.encode()),"increment_bytes":len(increment.encode()),"new_claims":ST["new_claims"],"open_count":ST["open_count"]},indent=2))
