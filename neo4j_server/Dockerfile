FROM neo4j:5.1.0
WORKDIR /var/lib/neo4j

RUN apt-get update && apt-get install -y nano && apt-get clean

ENV NEO4J_server_memory_pagecache_size=16G
ENV NEO4J_server_memory_heap_initial__size=8G
ENV NEO4J_server_memory_heap_max__size=16G
ENV NEO4J_db_memory_pagecache_warmup_enable=true

ENV NEO4J_server_unmanaged__extension__classes=n10s.endpoint=/rdf
ENV NEO4J_PLUGINS='["apoc", "n10s"]'
ENV NEO4J_AUTH=neo4j/password

ADD init-pipeline.sh init-pipeline.sh
ADD init-rdf.sh init-rdf.sh
ADD import-yago4.sh import-yago4.sh
ADD exclude.txt exclude.txt
ADD yago4_files.txt yago4_files.txt
