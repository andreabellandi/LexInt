#!/usr/bin/env python3
"""Controllo riproducibile del pacchetto RDF 1.2 LexInt.

Dipendenza: RDFLib >= 7.0. Le triple RDF 1.2 sono lette dal sorgente Turtle
mediante una trasformazione in memoria, strettamente limitata alle reificazioni
rdf:reifies <<(s p o)>> usate in questo pacchetto. Si interrogano equivalenti
RDF 1.1 delle query SPARQL 1.2, senza modificare i file distribuiti.
Questa NON e' una validazione nativa di RDF 1.2, SPARQL 1.2 o SHACL 1.2.
"""
from __future__ import annotations
from pathlib import Path
from collections import Counter
import csv, io, json, re
from rdflib import Graph, RDF, Namespace, URIRef

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'risultati'
LEX = Namespace('https://lexo.ilc.cnr.it/vocabulary/lexical-interpretation#')
PROV = Namespace('http://www.w3.org/ns/prov#')
DC = Namespace('http://purl.org/dc/terms/')
CRMINF = Namespace('http://www.cidoc-crm.org/extensions/crminf/')

# This converter only accepts a flat triple-term IRI/PName pattern, which is
# sufficient for the exact 31 reifications here. If it cannot recognize a
# token, it will fail; it does not silently invent triples.
TRIPLE_TERM = re.compile(r'rdf:reifies\s*<<\(\s*([^\s()]+)\s+([^\s()]+)\s+([^\s()]+)\s*\)>>')
VERSION = re.compile(r'^\s*VERSION\s+"1\.2"\s*$', re.M)

def normalize(text: str, *, is_query: bool) -> tuple[str, int]:
    text, versions = VERSION.subn('', text)
    if versions != 1:
        raise ValueError(f'Expected one VERSION 1.2 directive; got {versions}')
    count=0
    def repl(match: re.Match) -> str:
        nonlocal count
        count+=1
        s,p,o=match.groups()
        return f'rdf:subject {s} ; rdf:predicate {p} ; rdf:object {o}'
    text=TRIPLE_TERM.sub(repl, text)
    if '<<(' in text or ')>>' in text:
        raise ValueError('Found an unrecognized RDF 1.2 triple term')
    if not is_query and 'rdf:reifies' in re.sub(r'(?m)^\s*#.*$', '', text):
        raise ValueError('Unexpected rdf:reifies syntax in Turtle')
    return text, count

rdf12_files=sorted((ROOT/'rdf12').glob('[0-9][0-9]_*.ttl'))
assert len(rdf12_files)==5
scenario_expected={'00_contesto_e_fonti.ttl':(0,0,0),
  '01_etimologie_concorrenti.ttl':(2,14,0),
  '02_corvetto_2009.ttl':(3,5,2),
  '03_segmentazione_semantica.ttl':(3,12,3),
  '04_revisione_treccani.ttl':(0,0,2)}
all_ttl=(ROOT/'rdf12'/'tutti_gli_scenari.ttl').read_text(encoding='utf8')
text, nterms=normalize(all_ttl, is_query=False)
assert nterms==31, f'31 RDF 1.2 term reifications expected, found {nterms}'
assert not re.search(r'\brdf:(?:subject|predicate|object)\s+', all_ttl), 'RDF 1.1 classic statement fields found in RDF 1.2 data'
g=Graph()
g.parse(data=text, format='turtle')
union=Graph()
for file in rdf12_files:
    body, count=normalize(file.read_text(encoding='utf8'), is_query=False)
    part=Graph(); part.parse(data=body, format='turtle')
    actual=(len(set(part.subjects(RDF.type,LEX.InterpretiveClaim))),
           len(set(part.subjects(RDF.type,LEX.TargetAssertion))),
           len(set(part.subjects(RDF.type,LEX.LexicographicDecision))))
    assert actual==scenario_expected[file.name], (file.name,actual)
    union+=part
assert set(g)==set(union), 'Aggregated graph not identical to five input modules'

# Invariants of the dataset (independently checked, not by SHACL engine).
claims=set(g.subjects(RDF.type,LEX.InterpretiveClaim))
targets=set(g.subjects(RDF.type,LEX.TargetAssertion))
decisions=set(g.subjects(RDF.type,LEX.LexicographicDecision))
assert (len(claims),len(targets),len(decisions)) == (8,31,7)
assert not list(g.triples((None,LEX.targetsAssertion,None))), 'Old property targetsAssertion still occurs'
errors=[]
for claim in claims:
    cand=set(g.objects(claim,LEX.targetAssertion))
    if not cand or not cand<=targets: errors.append(f'Invalid claim-target association: {claim}')
    if not (list(g.objects(claim,DC.description)) or list(g.objects(claim,CRMINF.J26_has_unambiguous_description))):
        errors.append(f'Undescribed claim: {claim}')

candidate_triples=[]
for target in targets:
    ss=list(g.objects(target,RDF.subject)); pp=list(g.objects(target,RDF.predicate)); oo=list(g.objects(target,RDF.object))
    if (len(ss),len(pp),len(oo)) != (1,1,1):
        errors.append(f'Target does not identify one triple: {target}')
        continue
    if not isinstance(pp[0],URIRef): errors.append(f'Invalid predicate: {target}')
    candidate_triples.append((ss[0],pp[0],oo[0]))
    if (ss[0],pp[0],oo[0]) in g: errors.append(f'Candidate materialized: {target}')
    if list(g.objects(target,RDF.type)).count(RDF.Statement):
        errors.append(f'Wrong RDF 1.1 rdf:Statement type: {target}')

valid_outcomes={LEX.adopted,LEX.rejected,LEX.suspended,LEX.replaced}
for decision in decisions:
    def field(path,one=False,expected_class=None):
        vals=list(g.objects(decision,path))
        if (not vals) or (one and len(vals)!=1):
            errors.append(f'Invalid decision field {path}: {decision}')
        if expected_class is not None:
            for value in vals:
                if (value,RDF.type,expected_class) not in g:
                    errors.append(f'Invalid class {expected_class} on {value}')
        return vals
    field(LEX.concernsClaim,one=True,expected_class=LEX.InterpretiveClaim)
    outcomes=field(LEX.decisionOutcome,one=True)
    if not set(outcomes)<=valid_outcomes: errors.append(f'Bad decision outcome: {decision}')
    field(LEX.appliesToVersion,one=True,expected_class=PROV.Entity)
    field(PROV.wasAssociatedWith,expected_class=PROV.Agent)
    field(DC.description)
assert not errors, '\n'.join(errors)
assert len(candidate_triples)==len(set(candidate_triples)), 'Duplicate candidate triple'

# Shapes and profile: parsed and checked for the exact bridges and RDF 1.2 shape constraint.
profile=Graph(); profile.parse(ROOT.parent/'ontology'/'lexint-profile.ttl',format='turtle')
shapes=Graph(); shapes.parse(ROOT.parent/'ontology'/'lexint-shapes.ttl',format='turtle')
SH=Namespace('http://www.w3.org/ns/shacl#')
assert (LEX.targetAssertion,RDF.type,URIRef('http://www.w3.org/2002/07/owl#ObjectProperty')) in profile
assert (LEX.targetsAssertion,RDF.type,None) not in profile
shape=LEX.CandidateShape
assert any((node,SH.nodeKind,SH.TripleTerm) in shapes for node in shapes.subjects(SH.path,URIRef(str(RDF)+'reifies')))

expected={'CQ1_etimologie':2,'CQ2_corvetto':2,'CQ3_segmentazione':3,
          'CQ4_treccani':2,'CQ5_sospesi_rifiutati':16,
          'CONTROLLO_fonti_Corvetto':1,
          'CONTROLLO_candidati_non_asseriti':False}
OUT.mkdir(exist_ok=True)
summary=[]
for name,n in expected.items():
    qtext=(ROOT/'queries_sparql12'/f'{name}.rq').read_text(encoding='utf8')
    q_normal, nq=normalize(qtext,is_query=True)
    result=g.query(q_normal)
    if name=='CONTROLLO_candidati_non_asseriti':
        flag=bool(result)
        assert flag == n, (name,flag,n)
        (OUT/f'{name}.csv').write_text('boolean\nfalse\n',encoding='utf8')
        (OUT/f'{name}.json').write_text(json.dumps({'boolean':flag},indent=2)+'\n',encoding='utf8')
        summary.append((name,'false',nq))
    else:
        rows=list(result)
        assert len(rows)==n,(name,len(rows),n)
        if name in ('CQ1_etimologie','CQ2_corvetto','CQ3_segmentazione','CQ4_treccani','CQ5_sospesi_rifiutati'):
            assert nq>=1, f'No triple-term match in {name}'
        headers=[str(x) for x in result.vars]
        with (OUT/f'{name}.csv').open('w',encoding='utf8',newline='') as f:
            writer=csv.writer(f); writer.writerow(headers)
            for row in rows: writer.writerow([str(v) if v is not None else '' for v in row])
        # Standards-conformant SPARQL 1.1 results JSON with lexical form and datatypes.
        js=json.loads(result.serialize(format='json').decode('utf8'))
        (OUT/f'{name}.json').write_text(json.dumps(js,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        summary.append((name,len(rows),nq))

report=['# Rapporto automatico di controllo - 19 novembre 2026',
        '', 'Formato sorgente: **RDF 1.2 Turtle** (`VERSION "1.2"`, triple terms via `rdf:reifies`).',
        'Query distribuite: **SPARQL 1.2**.',
        '', f'- Triple RDF 1.2 effettive (metadati, non candidate assertive): **{len(g)-2*nterms}**',
        f'- Triple del grafo equivalente normalizzato RDF 1.1: **{len(g)}**',
        f'- InterpretiveClaim: **{len(claims)}**',f'- TargetAssertion: **{len(targets)}**',
        f'- LexicographicDecision: **{len(decisions)}**',
        f'- Triple term candidate individuate: **{nterms}**',
        '- Proposizioni candidate materializzate: **0**',
        '- Vincoli strutturali controllati da script: **nessuna violazione**',
        '- Confronto del file aggregato con i 5 moduli: **identici**',
        '- Profilo e shapes Turtle leggibili: **si**', '',
        '## Righe restituite', '', '| Query | Righe / risposta | Triple pattern 1.2 tradotti in memoria |',
        '|---|---:|---:|']
report += [f'| {name} | {count} | {nq} |' for name,count,nq in summary]
report += ['', '**Metodo e limitazione.** Il presente runtime non dispone di un motore '
          'RDF 1.2/SPARQL 1.2 e SHACL 1.2 nativo. Per produrre i CSV/JSON, '
          'lo script legge i Turtle RDF 1.2 di questo pacchetto e converte '
          '**in memoria** le 31 triple term `rdf:reifies` in una rappresentazione '
          'RDF 1.1 strutturalmente equivalente; converte analogamente i pattern '
          'delle query e li esegue con RDFLib. Verifica inoltre i vincoli dei '
          'node shape con controlli dedicati. Questi controlli NON sostituiscono '
          'un test di esecuzione nativo RDF/SPARQL/SHACL 1.2.', '',
          'Riproduzione: `python documentazione/verifica_e_genera_risultati.py` '
          '(richiede `rdflib >= 7`).', '']
(ROOT/'documentazione'/'VALIDAZIONE.md').write_text('\n'.join(report),encoding='utf8')
(OUT/'SINTESI.md').write_text('\n'.join(report),encoding='utf8')
print('Verifica completata:', 'triples',len(g), 'targets',nterms)
for x in summary: print(x)
