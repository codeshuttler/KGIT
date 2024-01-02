#!/bin/bash
# Download YAGO4 data
pushd ./neo4j_server
if [ -e ./logs/label_download_yago4.txt ]
then
    echo "yago4 data downloaded"
else
    echo "Downloading yago4 data..."
    /bin/bash download-yago4.sh ./yago4_files.txt
    
    retVal=$?
    if [ $retVal -ne 0 ]; then
        echo "Error download YAGO4 data."
        exit $retVal
    fi

    touch ./logs/label_download_yago4.txt
fi
popd

# Start neo4j server
BUILDKIT_PROGRESS=plain DOCKER_UID=$UID DOCKER_GID=$GID docker-compose build neo4j
BUILDKIT_PROGRESS=plain DOCKER_UID=$UID DOCKER_GID=$GID docker-compose up neo4j -d

sleep 10s
# init rdf
docker exec -u root -t neo4j_server /bin/bash init-pipeline.sh
