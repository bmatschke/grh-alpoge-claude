#!/usr/bin/env python3
"""Write the substantive current report from the exact increment ledger."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
def read(name): return json.loads((ROOT/name).read_text())
cfg=read('increment_v0_52.json'); st=read('integration_stats_v0_52.json')
coverage=read('dependency_audit_v0_52/route_coverage.json')
reg=read('dependency_audit_v0_52/remaining_leaf_register.json')
out=['RH AND UNRESTRICTED DIRICHLET GRH — HUMAN RECONSTRUCTION v0.52',cfg['title'],'23 November 2026','',
 '1. RESULT OF THIS CONTINUATION','',cfg['status'],'',
 'This continues v0.51. The accepted formal proof remains the source of the intended statements; the task is their readable mathematical reconstruction. '
 'All 3192 predecessor claim records and the entire historical cumulative proof body are preserved. '
 'The four new chapters contain GSL1–GSL26, AFE1–AFE21, BQS1–BQS23 and SSC1–SSC17: 87 independently reviewed claims. '
 'The cumulative inventory is 3279. No additional whole selected obligation is closed; 24 remain. '
 'This distinction is substantive: full local Bessel nonvanishing, for example, does not yet construct the global normalized spectral family estimate.','',
 '2. READING ORDER','',
 'RH_new_proofs_v0_52.tex contains the current audit and all four new chapters. RH_readable_reconstruction_v0_52.tex contains the cumulative manuscript, including CMP1–CMP6, the inherited conditional terminal RH/Dirichlet-GRH deduction. '
 'The roadmap identifies the remaining mathematics and exact source entries; the parallel plan divides the next work into bounded assignments. Individual proof chapters are:','']
for comp in cfg['components']:
 p=read(comp+'/provenance.json'); ids=[c['id'] for c in p['claims']]
 out+=['  '+ids[0]+'–'+ids[-1]+': '+comp+'/main.tex']
out+=['','3. THE NEW MATHEMATICS','']
titles=['Universal bases and the full conditional section laws','Full arithmetic entries and representation descent','Both Bessel quotients and full local nonvanishing','The complete Selmer-signature comparison']
for i,(title,t) in enumerate(zip(titles,cfg['local_conclusions']),1):out += [f'3.{i}. {title}','',t,'']
out+=['4. THE MAIN SIMPLIFICATIONS AND WHY THEY PRESERVE THE SCOPE','',
 'A finite identity gives all base changes at once. Suppose the relevant section complex has matrices D0 and D1 and is exact in the middle over the chosen field. GSL3 constructs B,C,H and r with D0*B=0, C*B=rI and B*C+H*D0=rI. '
 'After any map making r a unit, every kernel vector v equals B*(r^(-1)C*v), and C*B=rI proves uniqueness. '
 'Thus the basis is not reconstructed separately for each test algebra. The same certificate works for nonflat coefficient changes and algebras with nilpotents. '
 'For the local twist law, r has nonzero residue, so it is a unit in the original local ring. Writing a residue section in the reduced basis and lifting its finitely many coefficients proves the full section-lifting statement. '
 'GSL5–GSL10 separately justify the passage from the supplied finite-projective section model to these literal matrices and coordinates. The geometric model producer remains a named task.','',
 'The Host branch keeps its actual dyadic information. AFE9 uses the order of a principal unit modulo a power of two and the original strict bound 8*o*p^2<2^c2 to force the needed character value. '
 'AFE10 combines this with a corrected local Frobenius and then squares it to obtain eta4=1 and a nonquadratic residual character, at every original allowed place. '
 'This includes ell=3. The later frame construction uses the already fixed character modulus and the same marked element g1; it does not reconstruct separate favorable frames for the finite and automorphic endpoints. '
 'AFE19 uses the closed actual Galois kernel and adic separatedness over a Noetherian local domain to descend the ordinary point. AFE20 then fixes G_L before all later coefficient algebras and points.','',
 'The Schmid-Casimir comparison uses a common diagonal compact type. In the BQS argument, place the given lowest compact type diagonally in the original target and the already constructed discrete-series model. '
 'Both coordinates satisfy the same negative first-layer coupling relation. The inherited finite-layer inequality DC9 therefore forces the original compact type to occur only in degree zero, with one highest line. '
 'The central Casimir sends its diagonal highest vector to a pair involving the two Casimir scalars. Uniqueness of that line forces the scalars to agree. '
 'Every orthogonal complement used here is finite dimensional, so completion of the target is unnecessary. The original h-2 margin is retained. This gives a shorter route to the minimal-type supplier without weakening its quantified target class.','',
 'The quotient keeps the actual period. BQS first proves the full generic quotient theorem, including its image and stability clauses, then specializes its stable kernel to the simultaneous kernel of all prescribed Bessel periods. '
 'Equality of smooth L2 classes gives equality of the relevant actual smooth functions on the unitary group and hence of their periods. '
 'The result supplies both directions of the actual image relation and period injectivity. BSE supplies explicit nonzero evaluated periods; together these now prove full StepStatement and BesselNVGap. '
 'Forms0 remains an input to the setting return, and the global measure, uniqueness and family-estimate producers remain explicit.','',
 'Arbitrary local DVR changes do not require finite residue extensions. For O->O-prime, SSC5 lifts a possibly infinite residue basis once and proves that it gives compatible coordinates in every quotient by pi^n. '
 'These coordinates identify the torsion fraction quotient with a direct sum of copies of K/O as an O-module. A continuous cocycle from a compact Galois group into a discrete module has finite image, hence involves finitely many basis coordinates. '
 'SSC6 therefore compares cocycles, coboundaries and every original local span coordinate by coordinate. The Selmer module is the actual scalar extension, and its length scales by the positive ramification index, including the infinite-length case. '
 'The denominator scales by the same factor. The source zero-denominator conventions are handled separately, rather than hidden in cancellation.','',
 'Crystalline lifts and rational boundaries stay separate at the broadest scope. The full SSC4 source theorem does not assume the matrix homomorphism is continuous. '
 'The corrected proof keeps c(g)=[z(g)+M(g)v-v], transports the continuous crystalline cocycle z and its period witness, and applies the coordinate map algebraically to v. '
 'The quotient coordinate of c is still a continuous cocycle. This proves the original coefficient-condition equality without assuming that the rational coboundary itself is continuous. '
 'The actual-family argument later has the stronger continuity it needs, but it is not imported into this broader theorem.','',
 'The signature uses the exact same character. SSC11 constructs one attached signature with all five SelCore fields; SSC12–SSC14 compare the tame conductor through the actual common place and normalized valuations. '
 'SSC16 then proves the full JointSix/SignatureChoice supplier. Its twist orientation is the one already fixed in DFD11, so the 1/ell^2 killing budget applies to that actual family. '
 'SSC17 consequently removes the Selmer comparison premise from DFD15. Only the coherent Wach HW/Fon/Cmp remains at that setup step; the local ConclF estimates are subsequent work.','',
 '5. PRECISE NEXT WORK','']
for i,t in enumerate(cfg['next_targets'],1):out += [f'{i}. {t}','']
out += [
 'The new Wach handoff records a useful scope distinction. The source exists_of_layers permits choosing a complete dependent Layers record at each Good(K,s,LL); it does not ask for an additional unspecified transition system between layers. '
 'What must be preserved is the single dependent Gamma/R/I/E/Mo/Cl/Cm record and all its internal lattice-map, Frobenius/Gamma, Herr-class and comparison identities. '
 'This narrows the next task to the actual record fields without adding an artificial compatibility obligation. See selmer_signature_comparison_v52/wach_next_handoff.txt.','',
 'The geometric handoff separates the actual section-cube model, polarization base change, geometric integrality, rank-one and growth, Serre/multiplication, and square-generator inputs. '
 'GSL26 has completed their conditional installation; it has not globally produced them. See global_section_laws_v52/next_source_handoff.txt. '
 'The analytic handoff continues from full Bessel nonvanishing to the actual setting and global comparison inputs.','',
 '6. COMPLETE OPEN SELECTED REGISTER','', 'Shared RH/Dirichlet-GRH obligations (17):','']
byid={r['id']:r for r in reg['records']}
for cid in coverage['shared_open_leaf_ids']:
 r=byid[cid];out+=['  '+cid+' — '+r['category']+' — '+r['title']]
out+=['','Additional unrestricted Dirichlet-GRH obligations (7):','']
for cid in coverage['dirichlet_grh_only_open_leaf_ids']:
 r=byid[cid];out+=['  '+cid+' — '+r['category']+' — '+r['title']]
out+=['','There are no RH-only open leaves. The graph remains 121 nodes and 161 edges, with 17 class-C and seven class-B open leaves. '
 'GLOBAL_LOCAL_GAIN remains fully closed from v0.49. RH_dependency_audit_v0_52.txt prints the full contracts, shared objects, current progress and source evidence.','',
 '7. INDEPENDENT REVIEW AND VERIFICATION','',
 'Geometry and arithmetic were independently read by the coordinator; the geometry author independently reviewed the Bessel chapter; the arithmetic author independently reviewed the Selmer chapter. '
 'Every final review is bound to the exact frozen main file and all numbered proof ranges. The review corrected the geometric composition notation, the Selmer normalization typesetting and, substantively, the unrestricted crystalline-coboundary handling described above. '
 'All corrections are included in the reviewed text. No self-review is counted as the independent mathematical review.','',
 'Repository: https://github.com/CocoSgt/riemann-hypothesis-lean',
 'Pinned source commit: '+cfg['source_commit'],'',
 f"The new claim ledger verifies {st['new_source_files_checked']} distinct pinned source files and {st['new_unique_source_ranges_checked']} exact source ranges. "
 'Each included source snapshot equals its pinned Git blob. Every new claim records exact source/proof ranges, dependencies and review. The source fixes the intended contract; the proof itself is written in the human chapter.','',
 'All 3192 earlier claim records and the full historical proof body remain unchanged. Displaced v0.51 root metadata and plans are frozen in history/version_0_51. '
 'Current status is governed by the v0.52 audit, roadmap and plan; older status paragraphs remain historical records.','',
 'The release includes configuration, integration, assembly, independent-review, TeX validation and packaging scripts. validation_v0_52.json records the exact preservation and release checks, including the separate independent integration audit. '
 'Two-pass draft TeX checks syntax, references and new overflow diagnostics. No PDF generation, PDF visual certification or Lean/kernel replay is claimed. '
 'The archive-wide SHA256SUMS and external delivery record identify the complete checkpoint. Continue from v0.52 with the original objects, embeddings, characters, measures and choice order.','']
dest=ROOT/'RH_reconstruction_progress_v0_52.txt';dest.write_text('\n'.join(out))
print(json.dumps({'report':dest.name,'words':len(dest.read_text().split()),'bytes':dest.stat().st_size}))
