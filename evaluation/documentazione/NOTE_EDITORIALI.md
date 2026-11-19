# Coerenza con la sezione 5 allegata (19 novembre 2026)

## Testo e figure NON modificati

Il PDF `sez5.pdf` non e' incluso tra gli artefatti rivisti: questa distribuzione aggiorna il pacchetto RDF/query/risultati e fornisce soltanto suggerimenti per il manoscritto.

1. In 5.1, la didascalia della Figura 2 descrive ciascuna ipotesi come «un'asserzione candidata», ma il testo e il dataset ne rappresentano **sette** ciascuna: sostituire con «un insieme di sette asserzioni candidate raccolte in un'unica lexint:InterpretiveClaim».
2. In 5.4, correggere `lexint:TargetsAssertion` (plurale e maiuscolo) in `lexint:TargetAssertion` quando ci si riferisce alla **classe**, e `lexint:targetAssertion` quando ci si riferisce alla **proprieta'**. Le due forme non sono intercambiabili.
3. In 5.2, precisare che la lettura del testo giornalistico originale e' mediata da di Valvasone (2023), non da una consultazione integrale dell'articolo Galli (2009). Nell'esempio rimane assente `frac:quotedText`.
4. In 5.2, le due alternative sono distinte nei descrittori delle claim e nel percorso inferenziale. Per rispettare il testo e Figura 3 sono conservate **due** proposizioni candidate per ogni proposta. Un collegamento candidato attestazione-senso sarebbe un'**estensione** che richiederebbe l'aggiornamento di figura, descrizione e conteggi delle CQ.
5. In 5.3, le tre strategie rappresentano opzioni editoriali, ma il possibile senso specializzato `:sensoVandalo` puo' coesistere con una delle altre segmentazioni: evitare una formula che implichi incompatibilita' logica universale.
6. In 5.4, `:attoValutazioneTreccani` e' una rappresentazione dimostrativa della valutazione *pubblicamente documentata*, non la prova di un deliberato processo interno formalizzato dall'editore.

## Proprieta' e RDF 1.2

- `lexint:InterpretiveClaim` aggrega piu' proposizioni.
- Ogni `lexint:TargetAssertion` denota una sola proposizione mediante `rdf:reifies <<( s p o )>>`.
- La mera presenza del triple term non asserisce la proposizione.
- `lexint:targetAssertion` e' sempre la proprieta' usata per associare una claim a ogni target.
- Le decisioni riguardano sempre una versione (`lexint:appliesToVersion`).
