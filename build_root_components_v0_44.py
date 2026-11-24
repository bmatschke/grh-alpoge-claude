#!/usr/bin/env python3
"""Bind the two root-authored v0.44 chapters to the accepted source pin."""
from pathlib import Path
import hashlib, json, re, subprocess

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'formal_source'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
AV='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
DENSE=AV+'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
ORD=AV+'HeckeAlgebras/OrdinaryHeckeCharacters/'
BUILD=AV+'BuildingsResidueChars/'
PHT=AV+'PadicHodgeTheory/'
TOR=AV+'ModularityArgument/CuspidalDescent/UnitaryTorusDescent/'
AB='src/Development/AbelianVarietyTheory/'

def sha(b): return hashlib.sha256(b).hexdigest()
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
cache={}
def source(path,first=1,last=None):
    if path not in cache:
        data=(SOURCE/path).read_bytes()
        assert data==subprocess.check_output(['git','-C',str(SOURCE),'show',PIN+':'+path]),path
        cache[path]=data
    data=cache[path]; lines=data.splitlines(keepends=True)
    last=len(lines) if last is None else last
    assert 1<=first<=last<=len(lines),(path,first,last,len(lines))
    part=b''.join(lines[first-1:last])
    return {'path':path,'line_start':first,'line_end':last,'file_sha256':sha(data),'sha256':sha(data),
      'range_sha256':sha(part),'range_bytes':len(part),'verified_equal_to_pinned_git_blob':True,
      'url':'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+path+f'#L{first}-L{last}'}
def d(name,a=1,b=None): return source(DENSE+name+'.lean',a,b)
def p(name,a=1,b=None): return source(PHT+name+'.lean',a,b)
def b(name,a=1,z=None): return source(BUILD+name+'.lean',a,z)

UPA={
 1:([],[d('PartU',43,80),b('IsUnramifiedAtTotallyRealOfInertiaLeRestrictionR'),b('IsSplitAtOfDecompositionLeRestrictionRange')]),
 2:(['UPA1'],[b('ExistsDescentToLevelGroupOfUnramified',9,63)]),
 3:(['UPA2'],[b('ExistsDescentToLevelGroupOfUnramified',64),source(AV+'WeilGroupCharacters/UniversalOrdinaryDeterminantRing.lean',99,108)]),
 4:([],[d('PartU',101,120)]),
 5:([],[d('TSatLoc'),source(ORD+'SatTUnif.lean')]),
 6:(['UPA5'],[source(ORD+'SatTUnif.lean'),source(AV+'HeckeAlgebras/Distinct.lean')]),
 7:(['UPA5','UPA6','UPA9','GUA12','GUA1'],[d('TSatFrobT'),d('PartU',81,102)]),
 8:([],[source(TOR+'TypeTor.lean'),source(TOR+'HasHTOf.lean')]),
 9:([],[b('ExistsConjInertiaDiagonalOfIsTypeWD')]),
 10:([],[d('OrdAtLOf',18,41),source(AV+'HeckeAlgebras/Distinct.lean')]),
 11:([],[b('HodgeTateWeightsOfLocalGlobal'),source(AV+'HeckeAlgebras/Distinct.lean')]),
 12:(['UPA10','UPA11','GUA2'],[d('OrdAtLOf',42),d('MkAtLT'),source(AV+'ModularityArgument/OrdinaryJacquetModules/AtLOf.lean')]),
 13:(['UPA1','UPA3','UPA4','LTP12','LTP19','LTP20','LTP21','GUA14','GUA18'],[d('PartU',43,102)]),
 14:(['UPA5','UPA6','UPA7','UPA12','UPA13','LTP7','LTP9','LTP11','LTP14','GUA15','GUA18'],[d('PartU',89,120),d('UnitaryPointProperties',29,47)]),
 15:(['UPA3','UPA4','UPA8','UPA9','UPA13','UPA14','LTP12','LTP14','LTP15','LTP17','LTP18','GUA15','GUA16','GUA17','GUA18'],[d('PartU',103,148),d('UnitaryHeckeData',38,58)]),
 16:(['UPA13','UPA14','UPA15','GUA17','GUA18'],[d('PartU',43)]),
 17:(['ITA2','ADP12','UPA16'],[d('AuTeichEx'),d('UnitaryPointProperties',48)]),
 18:(['UPA17','AFS22','AFS20','AFS21'],[d('TJDense'),d('UnitaryHeckeData',59)])
}
OFL={
 1:([],[p('OrdCharIff'),d('LocOrdFlag',82,101),source(AV+'HeckeAlgebras/Distinct.lean'),source(AB+'Proofs/InertiaEigenvalues/GlobalArtinLocalIdeleInjective.lean',26,44),source(AB+'Proofs/InertiaEigenvalues/ExistsGlobalApproxOfArtinTrivial.lean',54,121),source(AB+'Proofs/InertiaEigenvalues/ValuationEqOneOfCongruentGlobalApprox.lean',49,181),source(AB+'Proofs/InertiaEigenvalues/EqOneOfApproxByCongruentGlobalUnits.lean',19,147),source(AB+'PublishedTheorems/GaloisCohomology₂/ChevalleyUnits.lean',7,10),source(AB+'PublishedTheorems/AutomorphicForms₂/ExistsUniqueHcharOfFiniteOrder.lean',24,39)]),
 2:([],[p('ExistsTotallyRealPrimitiveElementPadicFiniteExt'),p('ExistsTotallyImaginaryPadicSqrt')]),
 3:(['OFL2'],[p('LaGlob'),p('LaHecke'),p('IsLocallyAlgebraicTransferOfPlaceIso')]),
 4:(['OFL1','OFL3','UPA11'],[d('LocCharDR'),p('LaDeRham'),p('ContinuousRankOneRep'),p('RankOneCharacterIsdRAndJumpsZero'),source(AB+'PublishedTheorems/GaloisGeometry₂/AlgebraicCharacterWD.lean')]),
 5:([],[p('InertiaEigenvectorExtendsOfDistinctCharacters')]),
 6:(['OFL5'],[p('InertiaEigenvectorExtendsOfDistinctCharacters'),d('LocOrdFlag',16,40)]),
 7:([],[p('ExistsInvariantVectorOfFiniteImageAveraging'),source(AB+'Definitions/AutomorphicMembership/FiniteDimensionalWdSpace.lean',109,151)]),
 8:([],[p('ExistsFrobeniusFixedPeriod'),b('WeilGroupDenseInGaloisGroup')]),
 9:([],[p('ExistsInvariantOfDpstPhiFixedOfNonnegWeights'),p('LineInv'),b('DdRLeFilAndInfFilEqBotOfHodgeTateMult')]),
 10:(['OFL5','OFL6','OFL7','OFL8','OFL9'],[d('LocOrdFlag',21,81),source(AB+'Definitions/AutomorphicMembership/FiniteDimensionalWdSpace.lean',109,151)]),
 11:([],[p('DeRhamRationalTwistByCharacter'),d('LocOrdFlag',105,115)]),
 12:([],[p('ExistsCommonEigenline'),p('DeRhamRationalOfConj'),p('DeRhamRationalOfExtensionByCharacter')]),
 13:(['OFL1','OFL4','OFL10','OFL11'],[d('LocOrdFlag',116,147)]),
 14:(['OFL4','OFL12','OFL13'],[d('LocOrdFlag',116,157),p('ExistsCommonEigenline')]),
 15:([],[d('LocOrdFlag',158)]),
 16:(['OFL10','OFL14','OFL15'],[d('LocOrdFlag',158),p('OrdFlag')])
}

SCOPES={
 'automorphic_installation_v44':{
  'endpoint':'Full original partX_alt/partU_alt, all sixteen PartAltAlt fields and all four UnitaryPointProperties; original AuTeichEx AutomorphicHeckeSet; bare same-ideal TJDense.',
  'original_inputs_retained':['Original HypothesesH\u2032, HidaSetting, level quotient V.pr, coefficient DVR, fixed iota, arbitrary admitted weight/basis and nonzero YOf.','Original local type and the original BaseChangeIsobaricN/RowT, local correspondence, classical representation and period foundations explicitly retained by LTP, BCS and GUA.','For TJDense, original IsJ and V.S\u2032=s.S; no additional AutomorphicHeckeSet supplier.'],
  'not_asserted':['Whole COUNT_II_SUPPORT, either complete rank-four Link, all-level HasAut or the remaining four Hida endpoints.','Unconditional automorphy of every part: the cuspidal conclusion retains exactly its original irreducibility premise.'],
  'method':'Actual quotient descent, original Frobenius inverse/Satake polynomial, full inertia-type comparison, all-bridge AtLT, and one common representation in all record fields.'},
 'ordinary_flags_v44':{
  'endpoint':'Full original hecke_char_de_rham_of_local_artin_above_l and ordFlag_alt, including the ordered HasFlag and every-bridge PotCrys conclusions.',
  'original_inputs_retained':['Original LiteratureRankNHypothesis fields aut.art, aut.chA, aut.chW, aut.berger and loc.chev, fixed iota, original local Artin map, every bridge and tied period model.','The source period-ring foundations, comparison/finite model/tensor/exactness/descent laws, fundamental crystalline intersection, and unramified rank-one crystalline comparison.','Original continuous representation, increasing labeled weights, pairwise distinct unit characters, OrdChar and DRat inputs; no semisimplicity assumption.'],
  'not_asserted':['A reconstruction of the named foundational published period theorems themselves.','Production of the Hecke eigencharacters before the separate HEP calculation.'],
  'method':'CM globalization of local weights, rank-one normalization, finite inertia projectors, faithful Frobenius-translate descent, Vandermonde averaging of a periodic period, fundamental period intersection, and induction by character lines.'}
}

gross={'claim':'UPA5','classification':'A','title':'Spherical Satake isomorphism at the exact original normalization',
 'authors':'Benedict H. Gross','source':'On the Satake isomorphism, Proposition 3.6, formula (3.14), Proposition 6.4; Haar normalization (2.5)',
 'url':'https://people.math.harvard.edu/~gross/preprints/sat.pdf','pages':[6,8,11],
 'hypotheses_checked':'Actual finite characteristic-zero local field, split GL_n, n>=1, hyperspecial GL_n(O), Haar volume one, smooth irreducible spherical complex representation, nonzero Satake parameters, every fixed vector and every uniformizer.',
 'normalization':'T_j=q^(j(n-j)/2)e_j(B); source al_j for all natural j uses min(j,n). UPA6 proves source heckePol; GUA12 and UPA7 fix arithmetic/geometric inverse.'}

for component,prefix,spec in [('automorphic_installation_v44','UPA',UPA),('ordinary_flags_v44','OFL',OFL)]:
    folder=ROOT/component; data=(folder/'main.tex').read_bytes(); lines=data.splitlines(keepends=True); claims=[]
    for number,(deps,refs) in spec.items():
        cid=prefix+str(number)
        first=next(i+1 for i,x in enumerate(lines) if x.strip()==('% BEGIN '+cid).encode())
        last=next(i+1 for i,x in enumerate(lines) if x.strip()==('% END '+cid).encode())
        block=b''.join(lines[first-1:last]); title=re.search(r'\\paragraph\{'+cid+r'\. (.*)\}\n',block.decode())[1]
        title=re.sub(r'\\texttt\{([^{}]*)\}',r'\1',title).replace('\\_','_')
        c={'id':cid,'title':title,'introduced_in':'0.44','classification':'A' if cid=='UPA5' else 'B',
          'status':'Precisely matched published theorem' if cid=='UPA5' else 'Complete human proof in the exact stated scope',
          'depends_on':deps,'proof_location':{'file':component+'/main.tex','label':'claim:'+cid,'line_start':first,'line_end':last,'sha256':sha(block),'file_sha256':sha(data),'bytes':len(block)},'sources':refs}
        if cid=='UPA5': c['published_application']=gross
        claims.append(c)
    ledger={'schema':'rh-human-component-provenance/1','artifact_version':'0.44','date':'2026-11-23','component':component,'source_commit':PIN,'main_tex_sha256':sha(data),**SCOPES[component],'claims':claims,'no_lean_replay':True}
    write(folder/'provenance.json',ledger)
    write(folder/'original_contracts.json',{'source_commit':PIN,'component':component,**SCOPES[component],'claims':[c['id'] for c in claims]})
    write(folder/'closure.json',{'artifact_version':'0.44','component':component,'main_tex_sha256':sha(data),'complete_nested_endpoints':SCOPES[component]['endpoint'],'whole_selected_leaf_closed':False,'boundary':SCOPES[component]['not_asserted']})
    write(folder/'retained_foundations.json',{'component':component,'main_tex_sha256':sha(data),'foundations':SCOPES[component]['original_inputs_retained'],'not_newly_reconstructed':True})
    if component.startswith('automorphic'): write(folder/'published_inputs.json',[gross])
    refs={}
    for c in claims:
        for s in c['sources']: refs[(s['path'],s['line_start'],s['line_end'])]=s
    write(folder/'source_manifest.json',{'source_commit':PIN,'ranges':list(refs.values()),'range_count':len(refs),'file_count':len({s['path'] for s in refs.values()})})
    report=[component+' — version 0.44','23 November 2026','',SCOPES[component]['endpoint'],'',SCOPES[component]['method'],'','ORIGINAL INPUTS RETAINED']+SCOPES[component]['original_inputs_retained']+['','SCOPE BOUNDARY']+SCOPES[component]['not_asserted']+['','PROOF CLAIMS']
    for c in claims:
        report += [c['id']+': '+c['title'],'Dependencies: '+', '.join(c['depends_on'])]
        report += ['  '+s['path']+f":{s['line_start']}–{s['line_end']}" for s in c['sources']]
    report += ['','Source pin: '+PIN,'Every cited source byte range is checked against the accepted pinned git blob.','Independent mathematical reviews are bound separately to the proof hashes.','No Lean build, kernel replay, or global RH/GRH completion assertion.']
    (folder/'report.txt').write_text('\n'.join(report)+'\n')
    print(json.dumps({'component':component,'claims':len(claims),'files':len({s['path'] for s in refs.values()}),'ranges':len(refs),'main_sha256':sha(data)}))
