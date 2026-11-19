# Rapporto automatico di controllo - 19 novembre 2026

Formato sorgente: **RDF 1.2 Turtle** (`VERSION "1.2"`, triple terms via `rdf:reifies`).
Query distribuite: **SPARQL 1.2**.

- Triple RDF 1.2 effettive (metadati, non candidate assertive): **312**
- Triple del grafo equivalente normalizzato RDF 1.1: **374**
- InterpretiveClaim: **8**
- TargetAssertion: **31**
- LexicographicDecision: **7**
- Triple term candidate individuate: **31**
- Proposizioni candidate materializzate: **0**
- Vincoli strutturali controllati da script: **nessuna violazione**
- Confronto del file aggregato con i 5 moduli: **identici**
- Profilo e shapes Turtle leggibili: **si**

## Righe restituite

| Query | Righe / risposta | Triple pattern 1.2 tradotti in memoria |
|---|---:|---:|
| CQ1_etimologie | 2 | 1 |
| CQ2_corvetto | 2 | 1 |
| CQ3_segmentazione | 3 | 2 |
| CQ4_treccani | 2 | 1 |
| CQ5_sospesi_rifiutati | 16 | 1 |
| CONTROLLO_fonti_Corvetto | 1 | 0 |
| CONTROLLO_candidati_non_asseriti | false | 1 |

**Metodo e limitazione.** Il presente runtime non dispone di un motore RDF 1.2/SPARQL 1.2 e SHACL 1.2 nativo. Per produrre i CSV/JSON, lo script legge i Turtle RDF 1.2 di questo pacchetto e converte **in memoria** le 31 triple term `rdf:reifies` in una rappresentazione RDF 1.1 strutturalmente equivalente; converte analogamente i pattern delle query e li esegue con RDFLib. Verifica inoltre i vincoli dei node shape con controlli dedicati. Questi controlli NON sostituiscono un test di esecuzione nativo RDF/SPARQL/SHACL 1.2.

Riproduzione: `python documentazione/verifica_e_genera_risultati.py` (richiede `rdflib >= 7`).
