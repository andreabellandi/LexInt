# LexInt — Lexicographic Interpretation Profile

**LexInt** is an interoperable Semantic Web application profile for representing **lexicographic interpretations as first-class, provenance-aware, queryable resources**. It connects linguistic evidence and scholarly interpretations to candidate RDF assertions, epistemic assessments, disagreements where documented, and version-specific editorial decisions. It reuses **OntoLex-Lemon, LemonEty, OntoLex-FrAC, HiCO, CRMinf, PROV-O, and RDF 1.2**, rather than replacing those vocabularies.

A central principle is to keep an **interpretive claim** separate from an **editorial decision** and from the **publication of an asserted lexical triple**. An `lexint:InterpretiveClaim` can refer to several `lexint:TargetAssertion` resources, each of which identifies *one* candidate triple by using `rdf:reifies` with an RDF 1.2 triple term. Mentioning the triple term does **not** assert that triple.

## LexInt ontology and SHACL shapes

The ontology defines the main classes (`lexint:InterpretiveClaim`, `lexint:TargetAssertion`, `lexint:LexicographicDecision`), the bridges between them, and a controlled scheme of editorial decision outcomes (`adopted`, `rejected`, `suspended`, `replaced`). The accompanying SHACL shapes constrain claim-to-target links, candidate reification, and version-scoped editorial decisions. The RDF 1.2 branch of the target shape uses `sh:TripleTerm` and therefore requires a compatible SHACL 1.2 engine for native validation.

- **[Download the LexInt ontology (Turtle)](ontology/lexint-profile.ttl)** · [View source](ontology/lexint-profile.ttl)
- **[Download the LexInt SHACL shapes (Turtle)](ontology/lexint-shapes.ttl)** · [View source](ontology/lexint-shapes.ttl)

These files are **research/evaluation drafts**, not a claim of a separately published stable vocabulary release. Both files include `dcterms:creator` metadata identifying the authors.

## Authors

- [Andrea Bellandi](https://www.ilc.cnr.it/people/andrea-bellandi-2/) — CNR Institute for Computational Linguistics (ILC).
- [Giulia Benotto](https://www.ilc.cnr.it/people/giulia-benotto-2/) — CNR Institute for Computational Linguistics (ILC).

## Evaluation: four scenarios for *maranza*

The dataset models competing interpretations and editorial choices around the Italian word *maranza*, using the RDF 1.2 `VERSION "1.2"` syntax. The shared [context and sources](evaluation/rdf12/00_contesto_e_fonti.ttl) define the lexical entry, cited evidence, reference sources, and dataset versions. **Load this shared file together with an individual scenario**; scenario 5.4 also reuses the two claims in 5.1. Alternatively load the [combined graph](evaluation/rdf12/tutti_gli_scenari.ttl) only.

The following Turtle and SPARQL listings are reproduced verbatim from the downloadable example files. CSV output is provided after each query; URI values are kept verbatim to preserve reproducibility.

### 5.1 — Competing etymologies

A dialect-based hypothesis and a derivation from the audio brand Marantz are recorded as **two claims with seven unasserted candidate triples each**, covering the complete LemonEty structure. Belief values are kept distinct from lexical assertions. The query identifies the hypotheses, their source documents, and the number of propositions.

**Files:** [RDF 1.2 Turtle](evaluation/rdf12/01_etimologie_concorrenti.ttl) · [SPARQL 1.2 query](evaluation/queries_sparql12/CQ1_etimologie.rq) · [CSV results](evaluation/risultati/CQ1_etimologie.csv) · [JSON results](evaluation/risultati/CQ1_etimologie.json). **Result:** 2 row(s).

<details>
<summary>Full RDF 1.2 Turtle example</summary>

```turtle
VERSION "1.2"
@prefix : <https://example.org/lexint/maranza/> .
@prefix lexint: <https://lexo.ilc.cnr.it/vocabulary/lexical-interpretation#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ontolex: <http://www.w3.org/ns/lemon/ontolex#> .
@prefix lemonEty: <http://lari-datasets.ilc.cnr.it/lemonEty#> .
@prefix frac: <http://www.w3.org/ns/lemon/frac#> .
@prefix hico: <http://purl.org/emmedi/hico/> .
@prefix crminf: <http://www.cidoc-crm.org/extensions/crminf/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix cito: <http://purl.org/spar/cito/> .
@prefix dcmitype: <http://purl.org/dc/dcmitype/> .

# Scenario 5.1. Sette proposizioni NON ASSERITE per ciascuna etimologia.
:claimEtyDialetto a lexint:InterpretiveClaim, prov:Entity ;
    dcterms:description "Ipotesi di origine dialettale (non dimostrata)."@it ;
    prov:wasGeneratedBy :attoEtyDialetto .
:claimEtyMarantz a lexint:InterpretiveClaim, prov:Entity ;
    dcterms:description "Ipotesi di derivazione dal marchio Marantz (non esclusiva)."@it ;
    prov:wasGeneratedBy :attoEtyMarantz .
:attoEtyDialetto a hico:InterpretationAct, prov:Activity ;
    prov:used :fonteBanfi1992, :fonteDiValvasone2023 ; prov:wasAssociatedWith :analista .
:attoEtyMarantz a hico:InterpretationAct, prov:Activity ;
    prov:used :fonteBisceglia2023 ; prov:wasAssociatedWith :analista .
:credenzaDialetto a crminf:I2_Belief ; crminf:J4_that :claimEtyDialetto ; crminf:J5_holds_to_be :possible .
:credenzaMarantz a crminf:I2_Belief ; crminf:J4_that :claimEtyMarantz ; crminf:J5_holds_to_be :possible .
:possible a crminf:I6_Belief_Value ; rdfs:label "possible"@en .
:etimoDialetto rdfs:label "Melanzana / ipotesi dialettale"@it .
:etimoMarantz rdfs:label "Marantz (marchio audio)"@it .

# Ogni lexint:TargetAssertion denota ESATTAMENTE una tripla candidata.
:targetEtyDialetto1 a lexint:TargetAssertion ; rdf:reifies <<( :maranza lemonEty:etymology :etyDialetto )>> .
:claimEtyDialetto lexint:targetAssertion :targetEtyDialetto1 .
:targetEtyDialetto2 a lexint:TargetAssertion ; rdf:reifies <<( :etyDialetto lemonEty:hasEtyLink :linkDialetto )>> .
:claimEtyDialetto lexint:targetAssertion :targetEtyDialetto2 .
:targetEtyDialetto3 a lexint:TargetAssertion ; rdf:reifies <<( :linkDialetto lemonEty:etySource :etimoDialetto )>> .
:claimEtyDialetto lexint:targetAssertion :targetEtyDialetto3 .
:targetEtyDialetto4 a lexint:TargetAssertion ; rdf:reifies <<( :linkDialetto lemonEty:etyTarget :maranza )>> .
:claimEtyDialetto lexint:targetAssertion :targetEtyDialetto4 .
:targetEtyDialetto5 a lexint:TargetAssertion ; rdf:reifies <<( :etyDialetto rdf:type lemonEty:Etymology )>> .
:claimEtyDialetto lexint:targetAssertion :targetEtyDialetto5 .
:targetEtyDialetto6 a lexint:TargetAssertion ; rdf:reifies <<( :linkDialetto rdf:type lemonEty:EtyLink )>> .
:claimEtyDialetto lexint:targetAssertion :targetEtyDialetto6 .
:targetEtyDialetto7 a lexint:TargetAssertion ; rdf:reifies <<( :etimoDialetto rdf:type lemonEty:Etymon )>> .
:claimEtyDialetto lexint:targetAssertion :targetEtyDialetto7 .
:targetEtyMarantz1 a lexint:TargetAssertion ; rdf:reifies <<( :maranza lemonEty:etymology :etyMarantz )>> .
:claimEtyMarantz lexint:targetAssertion :targetEtyMarantz1 .
:targetEtyMarantz2 a lexint:TargetAssertion ; rdf:reifies <<( :etyMarantz lemonEty:hasEtyLink :linkMarantz )>> .
:claimEtyMarantz lexint:targetAssertion :targetEtyMarantz2 .
:targetEtyMarantz3 a lexint:TargetAssertion ; rdf:reifies <<( :linkMarantz lemonEty:etySource :etimoMarantz )>> .
:claimEtyMarantz lexint:targetAssertion :targetEtyMarantz3 .
:targetEtyMarantz4 a lexint:TargetAssertion ; rdf:reifies <<( :linkMarantz lemonEty:etyTarget :maranza )>> .
:claimEtyMarantz lexint:targetAssertion :targetEtyMarantz4 .
:targetEtyMarantz5 a lexint:TargetAssertion ; rdf:reifies <<( :etyMarantz rdf:type lemonEty:Etymology )>> .
:claimEtyMarantz lexint:targetAssertion :targetEtyMarantz5 .
:targetEtyMarantz6 a lexint:TargetAssertion ; rdf:reifies <<( :linkMarantz rdf:type lemonEty:EtyLink )>> .
:claimEtyMarantz lexint:targetAssertion :targetEtyMarantz6 .
:targetEtyMarantz7 a lexint:TargetAssertion ; rdf:reifies <<( :etimoMarantz rdf:type lemonEty:Etymon )>> .
:claimEtyMarantz lexint:targetAssertion :targetEtyMarantz7 .
```

</details>

<details>
<summary>SPARQL 1.2 query and results</summary>

```sparql
VERSION "1.2"
# SPARQL 1.2, triple terms non assertivi
PREFIX : <https://example.org/lexint/maranza/>
PREFIX lexint: <https://lexo.ilc.cnr.it/vocabulary/lexical-interpretation#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
PREFIX lemonEty: <http://lari-datasets.ilc.cnr.it/lemonEty#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX frac: <http://www.w3.org/ns/lemon/frac#>
PREFIX hico: <http://purl.org/emmedi/hico/>
PREFIX crminf: <http://www.cidoc-crm.org/extensions/crminf/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX cito: <http://purl.org/spar/cito/>

# Quali etimologie sono state proposte per maranza e con quali fonti?
SELECT ?claim ?etimologia (COUNT(DISTINCT ?tutte) AS ?numeroProposizioni)
       (GROUP_CONCAT(DISTINCT STR(?fonte); separator=" | ") AS ?fonti)
WHERE {
  ?claim a lexint:InterpretiveClaim ; lexint:targetAssertion ?target ; prov:wasGeneratedBy ?atto .
  ?target rdf:reifies <<( :maranza lemonEty:etymology ?etimologia )>> .
  ?atto prov:used ?fonte .
  ?claim lexint:targetAssertion ?tutte .
}
GROUP BY ?claim ?etimologia
ORDER BY ?claim
```

```csv
claim,etimologia,numeroProposizioni,fonti
https://example.org/lexint/maranza/claimEtyDialetto,https://example.org/lexint/maranza/etyDialetto,7,https://example.org/lexint/maranza/fonteBanfi1992 | https://example.org/lexint/maranza/fonteDiValvasone2023
https://example.org/lexint/maranza/claimEtyMarantz,https://example.org/lexint/maranza/etyMarantz,7,https://example.org/lexint/maranza/fonteBisceglia2023
```

</details>

### 5.2 — The 2009 Corvetto attestation

One attestation is separated from its mediated documentary source and from its interpretation. Two inferences suggest either a **separate lexical sense** or a **context-dependent reading of a broader sense**. Both editorial decisions are suspended. The example does not equate a context-bound ethnicized characterization with an established lexical definition.

**Files:** [RDF 1.2 Turtle](evaluation/rdf12/02_corvetto_2009.ttl) · [SPARQL 1.2 query](evaluation/queries_sparql12/CQ2_corvetto.rq) · [CSV results](evaluation/risultati/CQ2_corvetto.csv) · [JSON results](evaluation/risultati/CQ2_corvetto.json). **Result:** 2 row(s).

<details>
<summary>Full RDF 1.2 Turtle example</summary>

```turtle
VERSION "1.2"
@prefix : <https://example.org/lexint/maranza/> .
@prefix lexint: <https://lexo.ilc.cnr.it/vocabulary/lexical-interpretation#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ontolex: <http://www.w3.org/ns/lemon/ontolex#> .
@prefix lemonEty: <http://lari-datasets.ilc.cnr.it/lemonEty#> .
@prefix frac: <http://www.w3.org/ns/lemon/frac#> .
@prefix hico: <http://purl.org/emmedi/hico/> .
@prefix crminf: <http://www.cidoc-crm.org/extensions/crminf/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix cito: <http://purl.org/spar/cito/> .
@prefix dcmitype: <http://purl.org/dc/dcmitype/> .

# Scenario 5.2: Galli 2009 fonte originale; di Valvasone 2023 mediazione documentaria.
# L'attestazione e' derivata da una citazione secondaria, NON da consultazione diretta.
# J22 indica l'oggetto testuale della comprensione (fonte originale come citata);
# prov:used registra i supporti realmente esaminati: mediazione e attestazione ricostruita.
# La presente attivita' NON implica lettura diretta della fonte primaria.
:letturaCorvetto a hico:InterpretationAct, crminf:I16_Meaning_Comprehension, prov:Activity ;
    crminf:J22_interpreted_meaning_of :fonteCorvetto2009 ;
    crminf:J23_interpreted_meaning_as :credenzaSignificato2009 ;
    prov:used :attCorvetto2009, :fonteDiValvasone2023 ;
    prov:wasAssociatedWith :analista .
:claimLetturaCorvetto a lexint:InterpretiveClaim, prov:Entity ;
    dcterms:description "La fonte giornalistica del 2009 associa il termine a persone descritte mediante categorie etnicizzate; cio' non dimostra un senso autonomo."@it ;
    prov:wasGeneratedBy :letturaCorvetto .
:categoriaEtnicizzata rdfs:label "Categorizzazione etnicizzata nel discorso giornalistico (ipotesi interpretativa)"@it .
:credenzaSignificato2009 a crminf:I13_Intended_Meaning_Belief ;
    crminf:J4_that :claimLetturaCorvetto ; crminf:J5_holds_to_be :possible .
:inferenzaAutonomia a hico:InterpretationAct, crminf:I5_Inference_Making, prov:Activity ;
    crminf:J1_used_as_premise :credenzaSignificato2009 ;
    crminf:J2_concluded_that :credenzaSenso2009Autonomo ; prov:wasAssociatedWith :analista .
:inferenzaContestuale a hico:InterpretationAct, crminf:I5_Inference_Making, prov:Activity ;
    crminf:J1_used_as_premise :credenzaSignificato2009 ;
    crminf:J2_concluded_that :credenzaSenso2009Contestuale ; prov:wasAssociatedWith :analista .
:claimSense2009Autonomo a lexint:InterpretiveClaim, prov:Entity ;
    dcterms:description "Opzione interpretativa: riconoscere come accezione autonoma l'impiego del 2009, anziche' ricondurlo al senso piu' generale."@it ;
    prov:wasGeneratedBy :inferenzaAutonomia .
:claimSense2009Contestuale a lexint:InterpretiveClaim, prov:Entity ;
    dcterms:description "Opzione interpretativa: ricondurre l'impiego del 2009 a un senso generale contestualizzato, senza introdurre una nuova accezione."@it ;
    prov:wasGeneratedBy :inferenzaContestuale .
:credenzaSenso2009Autonomo a crminf:I2_Belief ; crminf:J4_that :claimSense2009Autonomo ; crminf:J5_holds_to_be :possible .
:credenzaSenso2009Contestuale a crminf:I2_Belief ; crminf:J4_that :claimSense2009Contestuale ; crminf:J5_holds_to_be :possible .
:decisioneSensoAutonomo a lexint:LexicographicDecision, prov:Activity ;
    lexint:concernsClaim :claimSense2009Autonomo ; lexint:decisionOutcome lexint:suspended ;
    lexint:appliesToVersion :versioneCorvettoDemo ; prov:wasAssociatedWith :analista ;
    dcterms:description "Decisione dimostrativa, non attribuita a un lessicografo storico."@it .
:decisioneSensoContestuale a lexint:LexicographicDecision, prov:Activity ;
    lexint:concernsClaim :claimSense2009Contestuale ; lexint:decisionOutcome lexint:suspended ;
    lexint:appliesToVersion :versioneCorvettoDemo ; prov:wasAssociatedWith :analista ;
    dcterms:description "Decisione dimostrativa, non attribuita a un lessicografo storico."@it .

# Ogni lexint:TargetAssertion denota ESATTAMENTE una tripla candidata.
# La specificita' delle due opzioni e' descritta nelle rispettive claim e inferenze.
# Per fedelta' alla Figura 3 (due target per opzione), non si introduce
# qui una sesta proposizione candidata di collegamento attestazione-senso.
:targetAttestazioneTema a lexint:TargetAssertion ; rdf:reifies <<( :attCorvetto2009 dcterms:subject :categoriaEtnicizzata )>> .
:claimLetturaCorvetto lexint:targetAssertion :targetAttestazioneTema .
:targetSense2009Type a lexint:TargetAssertion ; rdf:reifies <<( :senso2009Autonomo rdf:type ontolex:LexicalSense )>> .
:claimSense2009Autonomo lexint:targetAssertion :targetSense2009Type .
:targetSense2009Link a lexint:TargetAssertion ; rdf:reifies <<( :maranza ontolex:sense :senso2009Autonomo )>> .
:claimSense2009Autonomo lexint:targetAssertion :targetSense2009Link .
:targetSenseGeneraleType a lexint:TargetAssertion ; rdf:reifies <<( :sensoGenerale rdf:type ontolex:LexicalSense )>> .
:claimSense2009Contestuale lexint:targetAssertion :targetSenseGeneraleType .
:targetSenseGeneraleLink a lexint:TargetAssertion ; rdf:reifies <<( :maranza ontolex:sense :sensoGenerale )>> .
:claimSense2009Contestuale lexint:targetAssertion :targetSenseGeneraleLink .
```

</details>

<details>
<summary>SPARQL 1.2 query and results</summary>

```sparql
VERSION "1.2"
# SPARQL 1.2, triple terms non assertivi
PREFIX : <https://example.org/lexint/maranza/>
PREFIX lexint: <https://lexo.ilc.cnr.it/vocabulary/lexical-interpretation#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
PREFIX lemonEty: <http://lari-datasets.ilc.cnr.it/lemonEty#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX frac: <http://www.w3.org/ns/lemon/frac#>
PREFIX hico: <http://purl.org/emmedi/hico/>
PREFIX crminf: <http://www.cidoc-crm.org/extensions/crminf/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX cito: <http://purl.org/spar/cito/>

# Quali ipotesi di senso derivano dal Corvetto 2009 e qual e' la catena documentaria?
SELECT DISTINCT ?claim ?senso ?esito ?fontePrimaria ?fonteMediatrice
WHERE {
  :letturaCorvetto a crminf:I16_Meaning_Comprehension ;
      crminf:J23_interpreted_meaning_as ?premessa .
  ?inferenza a crminf:I5_Inference_Making ;
      crminf:J1_used_as_premise ?premessa ;
      crminf:J2_concluded_that ?credenza .
  ?credenza crminf:J4_that ?claim .
  ?claim lexint:targetAssertion ?target .
  ?target rdf:reifies <<( :maranza ontolex:sense ?senso )>> .
  ?decisione lexint:concernsClaim ?claim ; lexint:decisionOutcome ?esito .
  :attCorvetto2009 frac:observedIn ?fontePrimaria ;
      prov:wasDerivedFrom ?fonteMediatrice .
  ?fonteMediatrice cito:cites ?fontePrimaria .
}
ORDER BY ?claim
```

```csv
claim,senso,esito,fontePrimaria,fonteMediatrice
https://example.org/lexint/maranza/claimSense2009Autonomo,https://example.org/lexint/maranza/senso2009Autonomo,https://lexo.ilc.cnr.it/vocabulary/lexical-interpretation#suspended,https://example.org/lexint/maranza/fonteCorvetto2009,https://example.org/lexint/maranza/fonteDiValvasone2023
https://example.org/lexint/maranza/claimSense2009Contestuale,https://example.org/lexint/maranza/sensoGenerale,https://lexo.ilc.cnr.it/vocabulary/lexical-interpretation#suspended,https://example.org/lexint/maranza/fonteCorvetto2009,https://example.org/lexint/maranza/fonteDiValvasone2023
```

</details>

### 5.3 — Alternative sense segmentation

Three hypotheses propose respectively **one broad sense (3 candidates)**, **two differentiated senses (6 candidates)**, or **a possible vandalism-related sense (3 candidates)**. All associated decisions are suspended; the alternatives need not be logically mutually exclusive.

**Files:** [RDF 1.2 Turtle](evaluation/rdf12/03_segmentazione_semantica.ttl) · [SPARQL 1.2 query](evaluation/queries_sparql12/CQ3_segmentazione.rq) · [CSV results](evaluation/risultati/CQ3_segmentazione.csv) · [JSON results](evaluation/risultati/CQ3_segmentazione.json). **Result:** 3 row(s).

<details>
<summary>Full RDF 1.2 Turtle example</summary>

```turtle
VERSION "1.2"
@prefix : <https://example.org/lexint/maranza/> .
@prefix lexint: <https://lexo.ilc.cnr.it/vocabulary/lexical-interpretation#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ontolex: <http://www.w3.org/ns/lemon/ontolex#> .
@prefix lemonEty: <http://lari-datasets.ilc.cnr.it/lemonEty#> .
@prefix frac: <http://www.w3.org/ns/lemon/frac#> .
@prefix hico: <http://purl.org/emmedi/hico/> .
@prefix crminf: <http://www.cidoc-crm.org/extensions/crminf/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix cito: <http://purl.org/spar/cito/> .
@prefix dcmitype: <http://purl.org/dc/dcmitype/> .

# Scenario 5.3: tre strategie descrittive, tutte sospese nella stessa versione.
# L'eventuale senso specifico di vandalismo non e' necessariamente incompatibile
# con una segmentazione a uno o due sensi: il profilo non implica esclusivita'.
:GiovaneOstentatoTrasgressivo rdfs:label "Giovane ostentato e trasgressivo"@it .
:TamarroAnniOttanta rdfs:label "Tamarro degli anni Ottanta"@it .
:GiovaneUrbanoContemporaneo rdfs:label "Giovane urbano contemporaneo"@it .
:AutoreAttiVandalici rdfs:label "Autore di atti vandalici"@it .
:claimSensoAutonomo a lexint:InterpretiveClaim, prov:Entity ;
    dcterms:description "Ipotesi di una sola accezione ampia riferita al giovane ostentato e trasgressivo."@it ;
    prov:wasGeneratedBy :attoSegmentazioneUnica .
:claim2Sensi a lexint:InterpretiveClaim, prov:Entity ;
    dcterms:description "Ipotesi di due accezioni, storica e contemporanea."@it ;
    prov:wasGeneratedBy :attoSegmentazioneDueSensi .
:claimSensoAttuale a lexint:InterpretiveClaim, prov:Entity ;
    dcterms:description "Ipotesi aggiuntiva di una nuova accezione riferita a chi compie atti vandalici; potenzialmente compatibile con altre segmentazioni."@it ;
    prov:wasGeneratedBy :attoSensoVandalo .
:attoSegmentazioneUnica a hico:InterpretationAct, prov:Activity ;
    prov:used :fonteDiValvasone2023 ; prov:wasAssociatedWith :analista .
:attoSegmentazioneDueSensi a hico:InterpretationAct, prov:Activity ;
    prov:used :fonteDiValvasone2023 ; prov:wasAssociatedWith :analista .
:attoSensoVandalo a hico:InterpretationAct, prov:Activity ;
    prov:used :fonteCronaca2026 ; prov:wasAssociatedWith :analista .
:decisioneSensoUnico a lexint:LexicographicDecision, prov:Activity ;
    lexint:concernsClaim :claimSensoAutonomo ; lexint:decisionOutcome lexint:suspended ;
    lexint:appliesToVersion :datasetVersionX ; prov:wasAssociatedWith :analista ;
    dcterms:description "Sospensione dimostrativa della proposta di segmentazione per la versione X, non attribuita a una redazione reale."@it .
:decisioneDueSensi a lexint:LexicographicDecision, prov:Activity ;
    lexint:concernsClaim :claim2Sensi ; lexint:decisionOutcome lexint:suspended ;
    lexint:appliesToVersion :datasetVersionX ; prov:wasAssociatedWith :analista ;
    dcterms:description "Sospensione dimostrativa dell'ipotesi a due sensi per la versione X, non attribuita a una redazione reale."@it .
:decisioneSensoAttuale a lexint:LexicographicDecision, prov:Activity ;
    lexint:concernsClaim :claimSensoAttuale ; lexint:decisionOutcome lexint:suspended ;
    lexint:appliesToVersion :datasetVersionX ; prov:wasAssociatedWith :analista ;
    dcterms:description "Sospensione dimostrativa dell'ipotetica accezione vandalismo per la versione X, non attribuita a una redazione reale."@it .

# Ogni lexint:TargetAssertion denota ESATTAMENTE una tripla candidata.
:targetSensoOstentatoType a lexint:TargetAssertion ; rdf:reifies <<( :sensoOstentato rdf:type ontolex:LexicalSense )>> .
:claimSensoAutonomo lexint:targetAssertion :targetSensoOstentatoType .
:targetSensoOstentatoLink a lexint:TargetAssertion ; rdf:reifies <<( :maranza ontolex:sense :sensoOstentato )>> .
:claimSensoAutonomo lexint:targetAssertion :targetSensoOstentatoLink .
:targetSensoOstentatoReference a lexint:TargetAssertion ; rdf:reifies <<( :sensoOstentato ontolex:reference :GiovaneOstentatoTrasgressivo )>> .
:claimSensoAutonomo lexint:targetAssertion :targetSensoOstentatoReference .
:targetSensoTamarroType a lexint:TargetAssertion ; rdf:reifies <<( :sensoTamarro rdf:type ontolex:LexicalSense )>> .
:claim2Sensi lexint:targetAssertion :targetSensoTamarroType .
:targetSensoTamarroLink a lexint:TargetAssertion ; rdf:reifies <<( :maranza ontolex:sense :sensoTamarro )>> .
:claim2Sensi lexint:targetAssertion :targetSensoTamarroLink .
:targetSensoTamarroReference a lexint:TargetAssertion ; rdf:reifies <<( :sensoTamarro ontolex:reference :TamarroAnniOttanta )>> .
:claim2Sensi lexint:targetAssertion :targetSensoTamarroReference .
:targetSensoContemporaneoType a lexint:TargetAssertion ; rdf:reifies <<( :sensoContemporaneo rdf:type ontolex:LexicalSense )>> .
:claim2Sensi lexint:targetAssertion :targetSensoContemporaneoType .
:targetSensoContemporaneoLink a lexint:TargetAssertion ; rdf:reifies <<( :maranza ontolex:sense :sensoContemporaneo )>> .
:claim2Sensi lexint:targetAssertion :targetSensoContemporaneoLink .
:targetSensoContemporaneoReference a lexint:TargetAssertion ; rdf:reifies <<( :sensoContemporaneo ontolex:reference :GiovaneUrbanoContemporaneo )>> .
:claim2Sensi lexint:targetAssertion :targetSensoContemporaneoReference .
:targetSensoVandaloType a lexint:TargetAssertion ; rdf:reifies <<( :sensoVandalo rdf:type ontolex:LexicalSense )>> .
:claimSensoAttuale lexint:targetAssertion :targetSensoVandaloType .
:targetSensoVandaloLink a lexint:TargetAssertion ; rdf:reifies <<( :maranza ontolex:sense :sensoVandalo )>> .
:claimSensoAttuale lexint:targetAssertion :targetSensoVandaloLink .
:targetSensoVandaloReference a lexint:TargetAssertion ; rdf:reifies <<( :sensoVandalo ontolex:reference :AutoreAttiVandalici )>> .
:claimSensoAttuale lexint:targetAssertion :targetSensoVandaloReference .
```

</details>

<details>
<summary>SPARQL 1.2 query and results</summary>

```sparql
VERSION "1.2"
# SPARQL 1.2, triple terms non assertivi
PREFIX : <https://example.org/lexint/maranza/>
PREFIX lexint: <https://lexo.ilc.cnr.it/vocabulary/lexical-interpretation#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
PREFIX lemonEty: <http://lari-datasets.ilc.cnr.it/lemonEty#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX frac: <http://www.w3.org/ns/lemon/frac#>
PREFIX hico: <http://purl.org/emmedi/hico/>
PREFIX crminf: <http://www.cidoc-crm.org/extensions/crminf/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX cito: <http://purl.org/spar/cito/>

# Quali organizzazioni semantiche sono state considerate e quali esiti hanno?
SELECT ?claim ?esito
       (COUNT(DISTINCT ?senso) AS ?numeroSensi)
       (COUNT(DISTINCT ?target) AS ?numeroProposizioni)
WHERE {
  ?decisione a lexint:LexicographicDecision ;
    lexint:appliesToVersion :datasetVersionX ;
    lexint:concernsClaim ?claim ;
    lexint:decisionOutcome ?esito .
  ?claim lexint:targetAssertion ?target .
  ?target rdf:reifies <<( ?s ?p ?o )>> .
  OPTIONAL {
    ?claim lexint:targetAssertion ?targetSenso .
    ?targetSenso rdf:reifies <<( :maranza ontolex:sense ?senso )>> .
  }
}
GROUP BY ?claim ?esito
ORDER BY ?claim
```

```csv
claim,esito,numeroSensi,numeroProposizioni
https://example.org/lexint/maranza/claim2Sensi,https://lexo.ilc.cnr.it/vocabulary/lexical-interpretation#suspended,2,6
https://example.org/lexint/maranza/claimSensoAttuale,https://lexo.ilc.cnr.it/vocabulary/lexical-interpretation#suspended,1,3
https://example.org/lexint/maranza/claimSensoAutonomo,https://lexo.ilc.cnr.it/vocabulary/lexical-interpretation#suspended,1,3
```

</details>

### 5.4 — Treccani's 2025 etymological revision

This scenario reuses the 5.1 etymological claims. Two public editorial communications are treated as evidence for a revision, with both proposals editorially retained but a **highly plausible** belief value assigned specifically to Marantz. Dataset versions and the upper bound of the revision interval are represented separately.

**Files:** [RDF 1.2 Turtle](evaluation/rdf12/04_revisione_treccani.ttl) · [SPARQL 1.2 query](evaluation/queries_sparql12/CQ4_treccani.rq) · [CSV results](evaluation/risultati/CQ4_treccani.csv) · [JSON results](evaluation/risultati/CQ4_treccani.json). **Result:** 2 row(s).

<details>
<summary>Full RDF 1.2 Turtle example</summary>

```turtle
VERSION "1.2"
@prefix : <https://example.org/lexint/maranza/> .
@prefix lexint: <https://lexo.ilc.cnr.it/vocabulary/lexical-interpretation#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ontolex: <http://www.w3.org/ns/lemon/ontolex#> .
@prefix lemonEty: <http://lari-datasets.ilc.cnr.it/lemonEty#> .
@prefix frac: <http://www.w3.org/ns/lemon/frac#> .
@prefix hico: <http://purl.org/emmedi/hico/> .
@prefix crminf: <http://www.cidoc-crm.org/extensions/crminf/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix cito: <http://purl.org/spar/cito/> .
@prefix dcmitype: <http://purl.org/dc/dcmitype/> .

# Scenario 5.4: decisioni attribuite a esiti PUBBLICAMENTE DOCUMENTATI,
# non a deliberazioni interne alla redazione; si riusano i claim di 5.1.
# :attoValutazioneTreccani e' una formalizzazione della posizione pubblicamente
# documentata, non una dichiarazione dell'esistenza di un processo interno noto.
:notaTreccaniPrima a prov:Entity ; dcterms:description "Versione precedente della nota etimologica"@it .
:notaTreccani2025 a prov:Entity ; prov:wasRevisionOf :notaTreccaniPrima ;
    dcterms:replaces :notaTreccaniPrima ;
    dcterms:description "Nota etimologica aggiornata entro il 6 ottobre 2025"@it .
:attoValutazioneTreccani a hico:InterpretationAct, crminf:I5_Inference_Making, prov:Activity, crm:E7_Activity ;
    prov:used :fonteTreccaniSet2025, :fonteTreccaniOtt2025 ;
    prov:wasAssociatedWith :redazioneTreccani ;
    crm:P4_has_time-span :intervalloRevisione2025 ;
    crminf:J2_concluded_that :credenzaTreccaniMarantz .
:intervalloRevisione2025 a crm:E52_Time-Span ;
    crm:P82b_end_of_the_end "2025-10-06T23:59:59"^^xsd:dateTime .
:credenzaTreccaniMarantz a crminf:I2_Belief ;
    crminf:J4_that :claimEtyMarantz ; crminf:J5_holds_to_be :highlyPlausible .
:highlyPlausible a crminf:I6_Belief_Value ; rdfs:label "highly plausible"@en .
:decisioneTreccaniMarantz a lexint:LexicographicDecision, prov:Activity ;
    lexint:concernsClaim :claimEtyMarantz ; lexint:decisionOutcome lexint:adopted ;
    lexint:appliesToVersion :notaTreccani2025 ; prov:wasAssociatedWith :redazioneTreccani ;
    dcterms:description "Inclusione editoriale dell'ipotesi Marantz; attribuzione ricostruita dalle risposte pubbliche Treccani."@it .
:decisioneTreccaniDialetto a lexint:LexicographicDecision, prov:Activity ;
    lexint:concernsClaim :claimEtyDialetto ; lexint:decisionOutcome lexint:adopted ;
    lexint:appliesToVersion :notaTreccani2025 ; prov:wasAssociatedWith :redazioneTreccani ;
    dcterms:description "Mantenimento dell'alternativa dialettale; attribuzione ricostruita da documentazione pubblica."@it .

# Ogni lexint:TargetAssertion denota ESATTAMENTE una tripla candidata.
```

</details>

<details>
<summary>SPARQL 1.2 query and results</summary>

```sparql
VERSION "1.2"
# SPARQL 1.2, triple terms non assertivi
PREFIX : <https://example.org/lexint/maranza/>
PREFIX lexint: <https://lexo.ilc.cnr.it/vocabulary/lexical-interpretation#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
PREFIX lemonEty: <http://lari-datasets.ilc.cnr.it/lemonEty#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX frac: <http://www.w3.org/ns/lemon/frac#>
PREFIX hico: <http://purl.org/emmedi/hico/>
PREFIX crminf: <http://www.cidoc-crm.org/extensions/crminf/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX cito: <http://purl.org/spar/cito/>

# Quali etimologie figurano nella revisione Treccani 2025 e quali valori epistemici?
SELECT DISTINCT ?claim ?etimologia ?esito ?valutazione ?precedente ?entro
WHERE {
  ?decisione a lexint:LexicographicDecision ;
     lexint:appliesToVersion :notaTreccani2025 ;
     lexint:concernsClaim ?claim ; lexint:decisionOutcome ?esito .
  ?claim lexint:targetAssertion ?target .
  ?target rdf:reifies <<( :maranza lemonEty:etymology ?etimologia )>> .
  :notaTreccani2025 prov:wasRevisionOf ?precedente .
  :attoValutazioneTreccani crm:P4_has_time-span/crm:P82b_end_of_the_end ?entro .
  OPTIONAL {
     :attoValutazioneTreccani crminf:J2_concluded_that ?credenza .
     ?credenza crminf:J4_that ?claim ; crminf:J5_holds_to_be ?valutazione .
  }
}
ORDER BY ?claim
```

```csv
claim,etimologia,esito,valutazione,precedente,entro
https://example.org/lexint/maranza/claimEtyDialetto,https://example.org/lexint/maranza/etyDialetto,https://lexo.ilc.cnr.it/vocabulary/lexical-interpretation#adopted,,https://example.org/lexint/maranza/notaTreccaniPrima,2025-10-06T23:59:59
https://example.org/lexint/maranza/claimEtyMarantz,https://example.org/lexint/maranza/etyMarantz,https://lexo.ilc.cnr.it/vocabulary/lexical-interpretation#adopted,https://example.org/lexint/maranza/highlyPlausible,https://example.org/lexint/maranza/notaTreccaniPrima,2025-10-06T23:59:59
```

</details>

### Cross-cutting competency question (CQ5)

The cross-cutting query lists candidate propositions associated with **suspended or rejected** editorial decisions in specific dataset versions. The example has **16 returned propositions**, all from the suspended alternatives in scenarios 5.2 and 5.3. Its code is in [CQ5 SPARQL 1.2](evaluation/queries_sparql12/CQ5_sospesi_rifiutati.rq); results: [CSV](evaluation/risultati/CQ5_sospesi_rifiutati.csv) · [JSON](evaluation/risultati/CQ5_sospesi_rifiutati.json).

Two additional checks are included: [documentary provenance of the Corvetto source](evaluation/queries_sparql12/CONTROLLO_fonti_Corvetto.rq) (one row) and [absence of candidate-triple materialization](evaluation/queries_sparql12/CONTROLLO_candidati_non_asseriti.rq) (`ASK` returns `false`).

### Download and reproduce the evaluation

Download all examples, ontology and scripts from GitHub using **Code → Download ZIP**, or clone this repository:

```bash
git clone https://github.com/andreabellandi/LexInt.git
cd LexInt
python -m pip install 'rdflib>=7'
python evaluation/documentazione/verifica_e_genera_risultati.py
```

The script checks the five scenario modules against the combined RDF 1.2 Turtle, counts **8 interpretation claims, 31 candidate target assertions and 7 lexicographic decisions**, checks that **none of the 31 candidate triples is asserted**, checks key profile/shape constraints, executes in-memory equivalents of CQ1–CQ5 and the two control queries, and regenerates the CSV/JSON files under `evaluation/risultati/`. Expected CQ row counts: **2, 2, 3, 2, 16**.

**Validation scope:** the included Python script uses RDFLib with a **restricted, checked in-memory transformation** from RDF 1.2 triple terms (`rdf:reifies <<(s p o)>>`) into structurally equivalent RDF 1.1 reification, and applies the same transformation to SPARQL 1.2 queries before executing them. This is **not native RDF 1.2/SPARQL 1.2 execution nor full SHACL 1.2 validation**. For methodology and caveats, see [validation report](evaluation/documentazione/VALIDAZIONE.md).

Relevant specifications: [RDF 1.2 Turtle](https://www.w3.org/TR/rdf12-turtle/), [SPARQL 1.2 Query](https://www.w3.org/TR/sparql12-query/), [SHACL 1.2 Core](https://www.w3.org/TR/shacl12-core/).

## Repository layout

```text
ontology/                              LexInt profile and SHACL shapes
evaluation/rdf12/                      Shared context + four scenarios + aggregate Turtle
evaluation/queries_sparql12/           Five competency queries + two controls
evaluation/risultati/                  CSV and JSON expected query outputs
evaluation/documentazione/             Reproducibility script and validation notes
```
