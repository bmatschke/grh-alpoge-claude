#!/usr/bin/env python3
"""Write a self-contained current audit and its matching cumulative TeX chapter."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent;AUD=ROOT/"dependency_audit_v0_40"
read=lambda p:json.loads(p.read_text())
cfg=read(ROOT/"increment_v0_40.json")
records=read(AUD/"remaining_leaf_register.json")["records"]
new=cfg["expected_new_claims"];total=cfg["predecessor_claim_count"]+new
def esc(s):
 return "".join({
 "\\":r"\textbackslash{}","_":r"\_\allowbreak{}","&":r"\&","%":r"\%","$":r"\$",
 "#":r"\#","{":r"\{","}":r"\}","~":r"\textasciitilde{}","^":r"\textasciicircum{}",
 "≤":r"$\le$","≥":r"$\ge$","→":r"$\to$","∩":r"$\cap$","κ":r"$\kappa$",
 "λ":r"$\lambda$","χ":r"$\chi$","𝒞":r"$\mathcal C$","Ψ":r"$\Psi$",
 "ε":r"$\varepsilon$","−":"-","/":r"/\allowbreak{}"}.get(c,c) for c in s)
sections=[
("Status and classification",f"""The selected original Raw support theorem is now reconstructed at h=0, a=n=4, k.g=0, under its original arithmetic assumptions. Its actual limiting ring, maps, module, support completion, quotient determinant, ordinary point, coefficient normalization and pro-ell descent have all been supplied. This removes the entire selected patching/normalization/descent dependency from the current open arithmetic work. It leaves the construction of the original ordinary and automorphic input packet as a separate earlier obligation.

The original comparison constructors exists_pkT, rowPk_nonempty and exists_moved with Copy/Coh are also reconstructed on their original given-data hypotheses. The same finite catalogue, integral lattices, maps, metrics, measures and period coordinates are used together. The initial common geometric member, its fitting and rational-test conditions, and the exact eta agreement for full ReadL still have to be supplied.

There are {new} new proof claims and {total} cumulative claims. The Alpoge–Claude Lean proof is accepted as fully checked and correct. The complete human RH/Dirichlet-GRH proof remains unfinished; every status in this audit describes our reconstruction.

The selected sufficient dependency graph retains 121 nodes and 161 logical edges. RH reaches 101 nodes and unrestricted Dirichlet GRH reaches 110; their union covers the graph. All 245 historical compound targets in 107 scope groups remain. No whole compound leaf closes in this version: 33 remain open, classified as 22 C, 9 B and 2 D. A compound obligation stays open until all its original simultaneous duties are supplied on the actual shared objects. These counts are not percentages of completion or a claim that no alternative proof could use fewer dependencies.

A means a direct published-theorem application with exact hypotheses checked. B means an elementary or moderately difficult argument that can be reconstructed independently; its proof status is recorded separately. C means a substantial argument still requiring reconstruction. D means a possible gap in our human understanding of the source, never an allegation of a defect in the assumed-correct Lean proof. There are no open A leaves: the checked applications are completed internal inputs. The D leaves remain AD_VANISH_K_MATCH and HOST_RIGID_S.

This current audit governs older frontier descriptions retained in the cumulative manuscript. Historical statements and their conditional proofs remain intact, and their later suppliers are identified by additive scope updates."""),
("I. Actual universal rings and specialization maps — PRG1–PRG24","""The first construction represents the source's full five-part tuple: a determinant polynomial law on the actual profinite cover, every ordered local character, the distinguished scalar parameter, the ordered root variables and the patching variables. Representing only traces would lose part of the universal property in the selected residue characteristic 3 and rank 4.

PRG2 first proves that every O-algebra map between the original complete local coefficient objects is automatically local, residue-compatible and adically continuous. Their Noetherian maximal ideals and finite residue fields make every Artin quotient finite. Thus the original determinant continuity condition agrees with the continuous deformation functor used in the published theorem.

The determinant representability input is Chenevier, Lemma 3.2, Proposition 3.3, Remark 3.5 and Proposition 3.7. We use Proposition 3.7 through condition F: every open subgroup has only finitely many homomorphisms to the residue prime field. The actual finitely generated profinite global cover satisfies this by finite-index Schreier generation. The local character applications use the original PhiCond on every open subgroup. This alternative does not require ell>n and is valid for ell=3,n=4.

The theorem is first stated over W(k), while the source retains its own complete coefficient DVR O. PRG4 constructs the compatible W(k)-to-O map by lifting a finite-field generator and its separable monic polynomial. PRG6 then constructs the relative universal object as an explicit proper quotient of O[[Z_1,...,Z_d]]. Its universal property is checked on every original IsCO target, without presuming O flat over W(k). Equal-characteristic targets and degree zero are treated separately.

Degree-one determinant laws are identified with characters. For each original local index, the required values on the literal subgroup mu are imposed by the corresponding character relations. A finite completed coproduct joins the global determinant and all constrained local-character rings. Adjoining the original scalar, root and patching variables yields the full RRObj. Any supplied universal object is uniquely isomorphic to this one through its entire tuple, so the later constructions work with the source's actual W.

The ordered splitting algebra is built by adjoining one root at a time. It is finite free before selecting the specified residual root factor. Henselian idempotent lifting selects the exact complete local factor, which is still finite free of positive rank over the original base. PRG17 identifies this factor with the source's literal formal-series quotient Sp; ordinary algebra generation by the actual roots is proved, not merely topological generation.

Finally every actual finite-level tuple and the specialization tuple are constructed in their original rings. The universal property gives every rho_N and pi. The section is evaluated on the literal Unit variable, original weight coefficients and patching variables. The identities rho_N(s(z))=s_N(z) and pi(s(z))=Bmap(lambda(cc(z))) hold for every power series z, by complete evaluation and continuity. Thus rrEx and rmapsEx are complete original constructors, with no changed root ordering, module or ideal J."""),
("II. Actual patched module and full support theorem — PMS1–PMS32","""PMS reconstructs the general module-patching argument and then installs it on the actual Taylor–Wiles system. The finite modules at level N are the source's supplied M_N with their given additive free presentation, original scalar action and original exponent arrays. The ring action is through the exact rho_N constructed in PRG. The one ultrafilter is the one already used by the full Lim construction in LIM.

At each finite depth, the source congruences give eventual compatible actions and quotient modules. Taking the same ultrafilter quotient at every depth, then the inverse limit, yields the actual patched module. The construction verifies finiteness and completeness and all required scalar identities. It does not replace the modules by unrelated free modules having only the same rank.

The two original quotient maps are patched together. Both compositions are exactly multiplication by the same original fEl factor. The eventual comparison is uniform over the ring scalars needed for the module structure. Separately, all six relation families enter the approximate annihilator argument: kernel, polarization, ordinary, inertia, characteristic-root and tame/root relations. Its single exponent is the original A.ex+1, with no unrecorded later choice.

The support argument retains two completions and their precise roles. Over the completed coefficient ring, quasiregularity and the finite free augmentation fiber give a finite free module over the formal-series parameter ring. The image of the actual completed ring in its endomorphism ring is finite and torsion free over that parameter ring. Consequently every minimal component of its support has dimension at least the coefficient dimension plus the number of parameters. The fiber comparison and faithful-flat passage through completion establish the exact source support and move fields.

At a normalized point, the coefficient map onto K and the literal Unit parameter sent to t give the coefficient-completion dimension 1+D. There are nq patching parameters, so the minimal support dimension is at least 1+D+nq. This count is later matched to the same point's D0=D+nq, rather than to a dimension obtained from another coefficient ring.

PMS15 proves the full original S5 theorem, including its move clause. PMS29 supplies the actual original PMod and S5 instance from the original all-level TWAut and the constructed maps. PMS30 proves piKer using an integral Cayley–Hamilton trace calculation; it does not divide by n!. PMS31 proves the full piSurj under the literal source GenBy hypothesis. PMS32 proves the exact equivalence between containment of the augmentation fiber's annihilator and containment of the same original J in a prime of the splitting target.

These results supply the limiting module and support theorem that v0.39 still treated as open. They consume the original finite-level automorphic packet. They do not construct that arithmetic packet, prove the four Hida endpoints, or replace the shared ideal required by the complete Count-II statement."""),
("III. Coefficient normalization and closed relations — BCN1–BCN25","""The normalization has to make the coefficient ring surject onto the point field and add a genuine Unit variable sent to the point parameter. BCN constructs one finite free unramified coefficient extension O' for an entire equal-cardinality finite point chain, using a single lifted finite-field polynomial. The actual new ring is Til(B)=(O' tensor_O B)[[s]].

Every residual datum and Pair field is checked after extension. The local subgroups are unchanged, polarization uses the same cyclotomic map, and each ordered ordinary relation has the same group factors in the same order. Dense generation is proved at every adic depth by truncating the new variable and approximating its finitely many coefficients through the original generators.

The base module and every auxiliary module are the exact tensor extensions of the old ones. Finite module presentations identify the two relevant coefficient-series constructions and preserve the original free bases, ranks and exponent arrays. Both comparison maps tensor through the same identifications. Their scalar, determinant, character, root and paired-composition laws remain exact, and every annihilator relation keeps the same exponent. Thus the complete Unit-parameter TWAut is constructed from the original empty-parameter packet.

Prime lifting and point lifting are coupled. Finite freeness gives faithful flatness and going down; integrality gives going up along a whole finite chain. For each prescribed lifted prime, the chosen finite-field polynomial splits in the same original point field. Evaluation therefore gives a map to the same K[[t]] with exactly that kernel on the coefficient tensor ring. The new formal variable goes to t, and the O'-map onto K is surjective. The underlying NP representation, Kap, eigenvalues, B1/B2 constants and quantifier order are unchanged.

The closed Cayley–Hamilton relations require more than an ordinary tensor identity. BCN16 first proves base change for all full polynomial-law Cayley–Hamilton coefficients by finite-support generic substitution. No factorial polarization is used. BCN17 handles a finite free local coefficient extension by coordinates in a fixed basis: all defining closed-ideal intersections commute, and cofinal adic depths N and cN use the same open normal subgroup.

For formal series, an element of the group algebra has one fixed finite group support. At coefficient degree r, membership in the closed ideal at depth N+r implies membership of that coefficient in the old ideal at depth N. The intersection of the old ideal with the fixed finite-support module is finitely generated by Noetherianity. These fixed generators assemble all series coefficients into a finite group-algebra expression. This proves the actual closed-ideal equality without introducing infinite group support.

BCN20 also gives a short independent descent of the exact source semisimple-ring predicate. If K tensor_k E is semisimple, every extended left ideal has a module retraction. A k-linear functional b:K->k with b(1)=1 composes that retraction to an E-linear retraction of the original left ideal. Therefore E is semisimple. This uses no finite-dimensionality premise. The precise complemented-left-ideal definition is checked against the mathlib commit pinned by the source.

A common overfield and the correctly oriented quotient surjection now transport the existential NonSS witness. The same trace-matrix tuples transport discriminant stability. BCN23 proves the full original Core=>CoreBC implication for every finite equal-cardinality point chain. BCN24 states the smaller consumer needed here: normalized Core only at h=0,a=n,g=0 already suffices for CoreBC at those same data. BCN25 composes it pointwise with the inherited pro-ell descent. No general arbitrary-chain Core theorem is required by the selected route."""),
("IV. The selected Core and Raw proof — SCI1–SCI13","""The central new join is a complete selected producer, not a theorem that continues to assume a patched ring, module or ordinary point. Start with the original normalized one-point Core data, including its supplied all-level TWAut, the source GenBy hypothesis, O onto K, and the Unit variable sent to t. Set n=a=4, k.g=0 and D0=D+4q. The exact conclusion is the source's one-point ChainConcl for the original ideal J.

Let R be the actual universal ring and I its ideal generated by the six source relation families. PMS30 shows I lies in ker(pi), so C=R/I is a proper complete local quotient. The full determinant on the profinite cover must descend through the actual global group quotient. Trace equalities alone would not justify that descent in characteristic 3.

SCI2 applies Chenevier's Theorem 2.22(ii) to the ordinary full Cayley–Hamilton quotient. The base C is henselian, the determinant is Cayley–Hamilton by construction, and its residual law is the split sum of the original distinct characters. Every residual block has rank one. The theorem supplies orthogonal idempotents e_i with diagonal corners C e_i and trace(c e_i)=c. No finite-module hypothesis on the whole algebra or ell>n assumption is introduced.

SCI3 proves the needed full-kernel consequence. If tr(yz)=0 for all y, then e_i y z e_i=0. The integral identity D(1+ab)=D(1+ba) follows by inserting u(t)=1+t(a-1), using (1+ub)u=u(1+bu), cancelling the polynomial D(u) whose constant term is 1, and evaluating t=1. After every scalar extension, this identity shows D(1+hze_i)=1. The full determinant-kernel criterion makes every ze_i belong to the kernel, and their sum is z. Thus the trace relation really kills the relevant group-kernel generators as a full polynomial law.

This constructs ooDet. The original kernel/polarization/ordinary/inertia relations then give every OoPair field, and cancellation of pullback through the surjective group-algebra map gives full ooMaps. The exact adic generation field follows from the universal five-part tuple and the earlier integral word identity. Every quotient generator is the actual determinant coefficient, character value, root, patching variable or scalar parameter.

Choose one prime P in the actual finite free splitting target S0 above p=ker(x.f). Lift both the initial prime q1 and the target prime q below that same P. The point map lifts to f':S0->K[[t]] with ker(f')=P. To see this, tensor the finite fraction-field extension S0/P over B/p with K((t)). Each generating root satisfies a polynomial already split by the original eigenvalues in K((t)); a residue field of the tensor therefore introduces no new elements. Integrality and the normal DVR K[[t]] put the image back in that same series ring.

The splitting roots map to the original distinct eigenvalues, possibly in a different order, so the original product fEl(1,U) is nonzero at the lifted point. The original point's eigenvalue list is not relabeled. All remaining OoPt fields follow from the same limit, quotient pair, ordered relations and normalization. Its point kernel is exactly the prime used for completion.

Now let C* be that exact completed local quotient and let S* be the support ideal supplied by PMS. The starting prime, since it contains J, gives a prime of C* containing S*. Choose a minimal prime Z over S* below it. The S5 dimension theorem gives dim(C*/Z)>=1+D0. On the other hand the actual full-block cotangent construction CRW2–CRW18 gives a surjection from a regular power-series domain of dimension 1+D0 onto C*.

A nonzero kernel, or a nonzero inverse image of Z, would lower the dimension. Equality therefore forces Z=0. Since S* is contained in Z, S*=0. Every target prime below the same point now contains S*. The exact fiber equivalence and the original annihilator/J equivalence give J contained in q.

This proves SCI12, the selected normalized Core. The original stable starting-prime and stable-or-thick target-prime assumptions remain in its statement, although the full-block dimension argument makes them unused internally. There is no need to reconstruct general NonssT or multi-point propagation for this selected endpoint.

SCI13 applies BCN24/25 and the original PQL descent to obtain the selected original Raw conclusion. The final B,J,K,f, point/Kap data and constant-before-truncation/eventual-level quantifiers are unchanged. Every patching, normalization and descent supplier required by this selected route is now available. The remaining Count-II arithmetic task is to produce its original ordinary/control/type data, four Hida endpoints and all-level same-J TWAut/HasAut on both original Links with one common coefficient threshold."""),
("V. The full common comparison constructors — PKT1–PKT30","""PKT constructs the original comparison package from the original geometric and analytic Inputs, Pins and Holds. It does not assume a conveniently chosen replacement Hilbert model. The positive rational Gram matrices are complexified with exactly the original integral lattice carriers, and the finite group algebra action is extended on its required center.

The finite type catalogue is constructed from the actual smooth admissible unitary representation. Finite-dimensional fixed-vector spaces permit orthogonal projection without completing the smooth representation. A minimal fixed-space argument supplies irreducible summands; their actual function models give the source finite types. The catalogue simultaneously covers both original row levels, with the direct and conjugate type conventions preserved.

Compact Schur unfolding, the original coefficient pairing and the actual class-sum formula determine the metric constants. Both ChT records are constructed with the exact jE,jM,jX ranges, inner products, transition adjoints and coordinate readings. The LfT target map has precisely the original square-root norm factor; its integral carrier is the original good integral lattice. The source embedding and conditional theta clause are checked on the exact restriction map. No existence of a theta extension is inferred from that conditional field.

The full RrT uses the original rational row basis and every embedding's frame. Dall is the dimension before the good cut, and the source only asks delp<=1. Period coordinate maps are explicit pullback/descent equivalences preserving the source's framed and unframed functions. No new period nonvanishing or scalar factorization is asserted.

The full RowPk construction chooses its one numerical record before every eta and later V,S,N,G. The conditional period scalar is fixed by uniqueness whenever the source supplies a nonzero witness. The two local-index functions are defined on canonical lattices and compared with every subsequently supplied rational model by exact localization and quotient-length isomorphisms. Weight integrality, tuple choices and the original Sha dictionary are supplied at the same time.

PKT21 proves full exists_pkT; PKT27 proves full rowPk_nonempty. PKT28–PKT30 copy the original realization to each fitting later stage, preserving the same finite group through its actual place-label isomorphism. Every original Pins/Holds clause, geometric witness, period, measure and metric survives. The same coordinate maps and catalogue are copied rather than selected anew. This gives full exists_moved with both Copy and Coh.

Together with RDR, these constructors supply Side0, ReadPk and the common pins on the same objects. Full ReadL still needs o.eta(j,v)=q.eta(j,v) at every required row and place. Equality of the copied etaOf with the original realized eta does not prove equality with an arbitrary later chosen eta. Initial common geometry and its Inputs/Pins/Holds/ExAt/InGeo, actual Fits/rational tests, eta agreement and the outer family/eventual/same-Bundle duties remain. The stronger second DivRows3 theta square remains separate."""),
("VI. Next work selected for its contribution to the final theorem","""The first arithmetic priority is now the original input packet for Count-II: ordinary/control/separating fibers, type/neatU/TThetaEx, the four Hida endpoints, and all-level same-J TWAut/HasAut. These suppliers must coexist on each of the two rank-four Links, with ell=3, the fixed complex embedding and one coefficient threshold chosen before every later coefficient ring. The selected Raw proof is ready to consume them. Reconstructing a general multi-point Core or NonssT branch would not remove the current selected dependency.

An independent high-contribution branch is the actual initial common geometric member and its primitive rational/Fits tests. The comparison, copy and reading algorithms are now proved; their remaining original premises must be produced together on one R/F. Exact eta agreement, the stored nonzero chain and group tie, MultEq support and actual base rows cannot be replaced by unrelated witnesses.

The shared quantitative branch remains: actual NBuilt/NdSpec and the original local projection square, denominator and retained-defect estimates, period height, local gain, normalized spectrum and compatible second-layer selection on the common family. Host/frame, parts/eigensystems/all-embedding logLam, HD/d3b and NEb remain visible in the register.

RH and two-primary targets retain Cases I/II/V. Unrestricted Dirichlet GRH additionally retains Case III, Seed IV and original rank-four chain propagation/descent. The selected one-point completion does not settle these additional character branches. The two D-class source-interface questions also remain localized and classified.

The audit below is a complete register of the remaining selected sufficient obligations. Each contract is copied verbatim from the current graph and keeps its current category. The archive also retains every original source range, proof hash, prior claim field, mathematical edge and historical target. Independent mathematical reviews bind all 124 new claims to the released text; syntax and provenance validation are separate checks, not substitutes for those reviews.""")
]
plain=[f"RH AND DIRICHLET-GRH HUMAN RECONSTRUCTION — v0.40\n22 November 2026\nSource commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"]
tex=[r"\section{Current dependency audit: actual patching, selected Raw, and common comparisons}",
 r"\label{sec:dependency-audit-v40}"]
for title,body in sections:
 plain.extend([title.upper(),body])
 tex.extend([r"\subsection{"+esc(title)+"}",esc(body)])
plain.append("VII. EVERY REMAINING SELECTED OBLIGATION")
tex.append(r"\subsection{Every remaining selected obligation}")
for i,n in enumerate(records,1):
 title=n.get("title",n.get("name",n["id"]))
 heading=f'{i}. {n["id"]} — {n["category"]} — {title}'
 plain.extend([heading,n["contract"]])
 tex.extend([r"\paragraph{"+esc(heading)+"}",esc(n["contract"])])
plain.append("VIII. CHECKED PUBLISHED APPLICATIONS AND DELIVERY MAP")
tex.append(r"\subsection{Checked published applications and delivery map}")
apps=read(AUD/"published_applications.json")["freshly_checked_applications"]
for item in apps:
 name=item.get("citation",item.get("source",item.get("title","The Stacks Project" if item.get("primary_url","").startswith("https://stacks.") else item["id"])))
 if not isinstance(name,str):name=json.dumps(name,ensure_ascii=False)
 theorem=item.get("theorem",item.get("theorem_or_lemma","; ".join(item.get("theorem_locators",[])) or item.get("statement_used","")))
 if not isinstance(theorem,str):theorem=json.dumps(theorem,ensure_ascii=False)
 url=item.get("url",item.get("source_url",item.get("primary_url","")))
 statement=item.get("precise_import",item.get("statement_used",""))
 checks=item.get("hypotheses_checked",item.get("hypothesis_checks",[]))
 if isinstance(checks,dict):checks=[str(k)+": "+str(v) for k,v in checks.items()]
 if isinstance(checks,str):checks=[checks]
 text=f'{item["id"]}: {name}. {theorem}'
 if url:text+="\n"+url
 if statement:text+="\nUsed statement: "+statement
 if item.get("additional_primary_urls"):text+="\nAdditional primary sources: "+"; ".join(item["additional_primary_urls"])
 if checks:text+="\nChecked: "+"; ".join(str(z) for z in checks)
 plain.append(text)
 tex.append(r"\paragraph{"+esc(item["id"])+"}"+esc(name+". "+theorem))
 if url:tex.append(r"\url{"+url+"}")
 if statement:tex.append(esc("Used statement: "+statement))
 for more in item.get("additional_primary_urls",[]):tex.append(r"\url{"+more+"}")
 if checks:tex.append(esc("Checked: "+"; ".join(str(z) for z in checks)))
end="""The complete deliverable is RH_readable_reconstruction_v0_40.tex. This self-contained audit is RH_dependency_audit_v0_40.txt. RH_reconstruction_v0_40.zip contains the cumulative manuscript, component chapters, all inherited checkpoints, exact source/proof ledgers, graph and target registers, independent reviews, validation and source-bound continuation notes.

The current next-step files are continuation_notes_v0_40/next_count_ii.txt, next_analytic_and_common.txt and next_division_and_readings.txt. These are source-anchored work plans, not extra closure claims. Source Lean correctness remains the standing assumption; no Lean build or replay was performed. No PDF was generated. Historical RF16 remains governed by DEX11."""
plain.append(end);tex.append(esc(end))
(ROOT/"RH_dependency_audit_v0_40.txt").write_text("\n\n".join(plain)+"\n")
(AUD/"main.tex").write_text("\n\n".join(tex)+"\n")
print("Wrote",len(records),"exact remaining contracts;",new,"new claims;",total,"cumulative.")
