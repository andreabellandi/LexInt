# LexInt evaluation dataset

This directory contains four demonstration scenarios encoded in RDF 1.2 Turtle, five competency-question queries encoded in SPARQL 1.2, the corresponding CSV and JSON results, and the validation script.

See the [repository README](../README.md) for complete embedded examples and execution instructions.

```bash
python -m pip install 'rdflib>=7'
python evaluation/documentazione/verifica_e_genera_risultati.py
```

**Important:** the provided script performs a constrained, checked in-memory conversion from RDF 1.2 triple terms to equivalent RDF 1.1 reification and queries with RDFLib. It is **not** a native RDF 1.2 / SPARQL 1.2 / SHACL 1.2 engine.
