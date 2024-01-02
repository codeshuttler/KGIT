#!/bin/bash
export NEO4J_IMPORT="${PWD}/import"
export NEO4J_DB_DIR=$NEO4J_HOME/data/databases/graph.db
ulimit -n 65535

echo "Importing"
${NEO4J_HOME}/bin/cypher-shell -u neo4j -p 'password' "CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE"
${NEO4J_HOME}/bin/cypher-shell -u neo4j -p 'password' "CALL n10s.graphconfig.init();"
