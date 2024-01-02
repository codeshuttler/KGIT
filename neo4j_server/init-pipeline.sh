#!/bin/bash
if [ -e /logs/label_init_rdf.txt ]
then
    echo "neo4j rdf plugin inited"
else
    echo "init neo4j rdf plugin"
    /bin/bash init-rdf.sh

    retVal=$?
    if [ $retVal -ne 0 ]; then
        echo "Error init rdf"
        exit $retVal
    fi
    touch /logs/label_init_rdf.txt
fi

if [ -e /logs/label_import_yago4.txt ]
then
    echo "yago4 data imported"
else
    echo "Importing yago4 data..."
    /bin/bash import-yago4.sh

    retVal=$?
    if [ $retVal -ne 0 ]; then
        echo "Error import"
        exit $retVal
    fi
    touch /logs/label_import_yago4.txt
fi
