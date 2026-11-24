#!/usr/bin/env python3
"""Audit the actual ordinary Hecke/support producers; this is not a proof claim."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
SRC=WORK.parent/'lean-source'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
AV='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
DT=AV+'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
WG=AV+'WeilGroupCharacters/'
PM=AV+'PatchingModules/'
HE=AV+'HeckeAlgebras/'
FO='src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/'
files={}
def sha(b): return hashlib.sha256(b).hexdigest()
def anchor(path,name):
    b=(SRC/path).read_bytes()
    assert b==subprocess.check_output(['git','-C',str(SRC),'show',PIN+':'+path])
    ls=b.splitlines(keepends=True)
    pat=r'^(?:(?:private|noncomputable|protected)\s+)*(?:theorem|def|abbrev|structure|class)\s+([^\s:{(]+)'
    starts=[(i,m.group(1)) for i,s in enumerate(ls,1) if (m:=re.match(pat,s.decode()))]
    hits=[(i,n) for i,n in starts if n==name or n.endswith('.'+name)]
    assert len(hits)==1,(path,name,hits)
    a,n=hits[0]
    z=min([i for i,_ in starts if i>a]or[len(ls)+1])-1
    while not ls[z-1].strip():z-=1
    cut=b''.join(ls[a-1:z])
    files[path]=dict(path=path,sha256=sha(b),bytes=len(b),lines=len(ls))
    return dict(path=path,declaration=n,line_start=a,line_end=z,sha256=sha(b),
                range_sha256=sha(cut),range_bytes=len(cut),
                url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{a}-L{z}')

specs=[
 ('ordinary_quotient','Complete source quotient interface',DT+'HidaU.lean','HidaUAlt',
  'For every fixed original s,V,c,n,r,B,Lambda,iota, produces one J with all six HidaPropsAlt fields and HasAut.'),
 ('full_constructor','Actual whole producer',DT+'THidaU.lean','hida_unitary_of_printed_hida',
  'Uses actual unitary Hecke data, an actual Hecke ideal, all six point/ring/density/twist properties, and auxiliary-level modules. Its HypothesesH-prime premise is not a single Hida theorem.'),
 ('props','The six fields',DT+'PointTheoremBaseObject.lean','HidaPropsAlt',
  'ring, dense, pt, end1, end2 and twist must hold for the same J and fixed iota.'),
 ('data','Actual type, weight and residual eigenpacket',DT+'HdEx.lean','nonempty_unitaryHeckeData',
  'Constructs an integral compact type, its exact universal weight character, and a residual Hecke eigenpacket.'),
 ('integral_type','Integral local type',DT+'TTypeEx.lean','exists_integral_type_for_residual_rep',
  'Exact IsTypeAlt for the given residual inertia characters; no arbitrary chosen local representation may replace it.'),
 ('weight_character','Universal weight normalization',DT+'TThetaEx.lean','exists_theta_is_weight_of_lam_obj',
  'Relates the unitary diagonal-torus character to the actual LamObj and its ordered local characters with cyclotomic normalization.'),
 ('residual_packet','Residual eigenpacket',DT+'TResEx.lean','exists_is_res_of_residual_rep_and_type',
  'Produces the actual congruences for all spherical and ordinary Hecke operators.'),
 ('ideal','Actual Hecke quotient map and kernel',DT+'ExistsHeckeIdeal.lean','exists_hecke_ideal',
  'If the localized ordinary module is zero, J is top. Otherwise produces a surjection from B onto the actual localized Hecke algebra, compatible with Lambda, determinant and local characters.'),
 ('finite_module','Finite algebra over its given weight algebra',HE+'OrdinaryHeckeCharacters/HiAlgUnit.lean','hiAlg',
  'Supplies finiteness, torsion-freeness, residual operator congruences, ordinary units and algebra generation after an actual HSet.Ax, IsWt and nonzero localized module are supplied.'),
 ('finite_control','Ordinary module and commuting operators',HE+'OrdinaryHeckeCharacters/HiComm.lean','hiComm',
  'Substantive finite-module/control input to hiAlg, on the exact ordinary function spaces and levels.'),
 ('ring','Full RingProps on the actual kernel',DT+'TJRing.lean','ring_props_of_is_j_unitary_hecke_data',
  'Requires both the actual finite Hecke module and a separating family of actual classical Galois points; upgrades to full determinant annihilation and polarized identities.'),
 ('weight_density','Every-weight density in the exact weight ring',DT+'TDenseU.lean','isDomain_and_denseWt_of_isTheta',
  'Universal-character coordinates must match all finite characters and every prescribed algebraic weight.'),
 ('density','Every-weight density of actual Hecke points',DT+'TJDense.lean','dense_of_is_j_unitary_hecke_data',
  'Uses weight normalization, dense weights and separation of the actual Hecke algebra by classical points.'),
 ('point','Automorphic-point membership in J',DT+'HeckePolyCoeffZero.lean','hecke_ideal_point_properties',
  'Actual unitary descent and the exact local ordinary/refinement and auxiliary-unramified conditions are needed; tangent vanishing alone does not put a point on J.'),
 ('point_interface','Exact point-membership assertion',DT+'PointTheoremBaseObject.lean','PointTheoremBaseObject',
  'For n=2..4, arithmetic x and continuous IsAutCsdA representation, unramified at v0 and all-pair non-cyclotomic ordered flags imply J <= ker x.'),
 ('ends','Arithmetic decomposition and classicality',DT+'JEnd.lean','decomposition_and_automorphicAway_of_isJ',
  'Produces ArithmeticPointDecomposition and IrrArithPointsAutomorphicAway; the Dense aliases do not weaken the quantifier to an arbitrary chosen dense set.'),
 ('decomposition_interface','Exact end1 alias',FO+'AdmissibleResidues/ArithmeticPointDecomposition.lean','ArithmeticPointDecomposition',
  'Every arithmetic J-point has an actual continuous semisimple representation, a Speh-type decomposition, and the stated weak Frobenius-root ratio when all multiplicities equal one.'),
 ('classicality_interface','Exact end2 alias',FO+'PlainTorsionPairs/IrrArithPointsAutomorphicAway.lean','IrrArithPointsAutomorphicAway',
  'Every irreducible arithmetic J-point has AutOffN at the specified auxiliary place, including its local-global window witness.'),
 ('twist','Twist stability of the same ideal',DT+'JTwistA.lean','twistOk_of_isJ',
  'Requires actual unitary twisting, local types and ordinary principal-series compatibility. Ring existence alone does not give this property.'),
 ('level','Actual auxiliary-level module family',DT+'TLevelU.lean','level_of_is_j_unitary_hecke_data',
  'Builds one TWBase and the actual level modules for every auxiliary prime set, with classical specializations.'),
 ('automorphy','From level modules to Taylor-Wiles automorphy data',DT+'THasAutOf.lean','has_automorphy_of_statement',
  'Converts LevelAlt and exact local representation theory to HasAut; not a mere existence statement for a cusp form.'),
 ('has_aut','Exact patched-module input',PM+'TaylorWilesObstructionBound.lean','HasAut',
  'For every TWGrp and TWPl supplies TWAut for the same universal Pair and ideal, with dimension n[F-plus:Q].'),
 ('pfromaut','Original characteristic-ell support producer',PM+'AutomorphicDetection/PfromAut.lean','pFromAut',
  'Norm, Choice, arithmetic Taylor-Wiles prime selection, first-order dual bound, obstruction bound and Raw patching combine to prove the entire PfromAut.'),
 ('pfromaut_interface','Exact PfromAut premise and conclusion',PM+'TaylorWilesObstructionBound.lean','PfromAut',
  'CohP, actual LocCFT, nontrivial residual cyclotomic character and HasAut imply P1core and P3core.'),
 ('p1','Characteristic-ell support clause consumed by the two-Link join',WG+'UniversalOrdinaryDeterminantRing.lean','P1core',
  'For every actual NiceI point on J, every prime below its kernel contains J. QX does not infer this from characteristic-zero adjoint vanishing.'),
 ('p3','Broader chain-propagation field',WG+'UniversalOrdinaryDeterminantRing.lean','P3core',
  'A field of full ModularAlt. QX checks that its selected two-Link PMEx join does not consume it; it is not promoted as proved.'),
 ('modu','Full older package assembly',DT+'CoefIsCoef.lean','modU_of_printsH',
  'Combines HidaUAlt with PfromAut. This source wrapper retains all-rank quantifiers and P3core beyond the selected rank-four join.'),
 ('unramified','Original input record',DT+'WsLink.lean','UnramifiedInputs',
  'coh/pr/modU/lev/lam/b0; KX supplies lev/lam/b0, BX supplies coh. Whole pr and modU are not installed by those facts.'),
 ('hypotheses','Scope of the printed literature package',DT+'AfDesc.lean',"HypothesesH'",
  'Extends a larger literal automorphy and real-form package by unitary descent, cyclic base change/descent, quaternion existence and cusp semisimplicity. Each consumed theorem needs its own hypothesis match.')
]
nodes=[]
for ident,title,path,name,role in specs:
    nodes.append(dict(id=ident,title=title,role=role,source=anchor(path,name),
                      status='source dependency traced; not promoted to a new human proof'))
out=dict(schema='rh-ordinary-support-dependency-audit/1',artifact_version='0.29',source_commit=PIN,
    scope='Exact finite dependency audit of the remaining ordinary modular quotient and characteristic-ell support producers. This is a sufficient producer route, not an exhaustive Lean graph.',
    nodes=nodes,source_files=list(files.values()),
    completed_suppliers=['KX2: full LevEx','KX3: full LocCFTAll','KX5: full LamEx',
                         'KX6: full PhiAll','KX8: full ProModularRingExists with its Pair antecedent',
                         'KX9: exact canonical weight-to-pair maps','BX8: full CohomologyHyp'],
    scope_separations=[
      'The universal Pair ring is not an ordinary Hecke quotient.',
      'A finite torsion-free quotient does not by itself supply classical-point separation or point membership.',
      'An automorphic seed is not a proof that an arbitrary point is on the same modular support.',
      'Characteristic-zero adjoint vanishing does not prove P1core in characteristic ell.',
      'The two-Link selected consumer only needs the rank-four objects specified by QX; no all-rank HidaUAlt or ModUAlt is promoted.'],
    rejected_shortcut=dict(
      reference='P. B. Allen, J. Newton and J. A. Thorne, Automorphy lifting for residually reducible l-adic Galois representations, II, arXiv:1912.11269v2, Theorem 4.1.',
      url='https://arxiv.org/abs/1912.11269',
      verified_conditions=['Residually Schur polarized deformation problem',
        'Specific local deformation/level conditions, genericity and residual primitivity',
        'ell > 3 and ell does not divide n'],
      mismatch='The literal Resid/Link/Fit/Deep interfaces do not themselves state this whole list. In particular polarization of a multiplicity-free sum does not require each constituent to be individually polarized. No implication supplying the missing hypotheses has been reconstructed, so this theorem is not installed as the source P1core supplier.'),
    validation=dict(source_anchor_count=len(nodes),source_file_count=len(files),
                    every_source_file_checked_against_pinned_git_blob=True,
                    new_mathematical_claims=0,no_kernel_replay=True))
(HERE/'audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
text='Version 0.29: the remaining ordinary support producer\n\n'
text+='This is a dependency audit, not a new proof or an assertion of a gap in the supplied Lean development. It records the actual arithmetic producer that remains after the completed universal-ring and adjoint chains.\n\n'
text+='The exact source endpoint HidaUAlt chooses one ideal J for each original datum, coefficient ring, universal determinant ring, weight object and fixed embedding. The same J must satisfy all six HidaPropsAlt fields and carry the Taylor-Wiles module package HasAut. The KX construction supplies the actual universal objects and their maps, but none of these automorphic-support assertions follows just from their universality.\n\n'
text+='Producer chain and scopes\n\n'
for n in nodes:
    text+=n['title']+'\n'+n['role']+'\n'+n['source']['url']+'\n\n'
text+='What the selected consumer needs\n\n'
text+='QX traces the two actual Link objects and their common coefficient threshold. Its PMEx construction can use rank-four HidaPropsAlt plus P1core on those exact objects; the broader P3core and the all-rank ModUAlt quantifier are not required by that selected construction. The final QX chapter gives the precise quantifier order and any separate descent inputs.\n\n'
text+='Why a nearby published theorem has not been substituted\n\n'
text+='Allen–Newton–Thorne, arXiv:1912.11269v2, Theorem 4.1, proves a closely related characteristic-ell support result under a residually Schur polarized problem, specified local/genericity/primitivity conditions, and ell>3 with ell not dividing n. The literal source interfaces do not state this whole hypothesis list. In particular, polarization of the sum permits its distinct constituents to be paired rather than individually polarized. No proof of the missing implications has been supplied here. The theorem is therefore recorded as a candidate for a narrower matched subcase, not as a proof of P1core.\n\n'
text+='Next complete producer to reconstruct\n\n'
text+='Construct the actual localized ordinary Hecke module, its commuting operators and exact determinant/character map, then prove all six properties for its kernel. For characteristic ell, reconstruct the original finite Taylor-Wiles module support argument, or supply a published theorem whose entire hypothesis list is proved on the two actual rank-four Link objects. A zero localized module gives J=top and is allowed in the source construction, but its automorphic-point membership assertion still has to be verified; it is not a shortcut to a useful support witness.\n\n'
text+='Checked anchors: '+str(len(nodes))+' in '+str(len(files))+' pinned source files.\n'
(HERE/'audit.txt').write_text(text)
print(json.dumps(out['validation'],indent=2))
