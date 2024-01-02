#!/bin/bash
export NEO4J_IMPORT="${PWD}/import"
export NEO4J_DB_DIR=$NEO4J_HOME/data/databases/graph.db
ulimit -n 65535

echo "Importing"
for file in ${NEO4J_IMPORT}/*.nt*; do
    # Extracting filename
    echo $file
    filename="$(basename "${file}")"
    echo "Importing $filename from ${NEO4J_IMPORT}"
    ${NEO4J_HOME}/bin/cypher-shell -u neo4j -p 'password' "CALL  n10s.rdf.import.fetch(\"file://${NEO4J_HOME}/import/$filename\",\"N-Triples\");"
done