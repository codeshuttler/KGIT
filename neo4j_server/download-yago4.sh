#!/bin/bash
set -e

export DATA_DIR="${PWD}/yago4_data"
export NEO4J_HOME=${PWD}/../neo4j_server
export NEO4J_IMPORT="${NEO4J_HOME}/import"
mkdir -p -v "${DATA_DIR}"
mkdir -p -v "${NEO4J_IMPORT}"

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters."
    exit 1
fi

if [ -d $DATA_DIR ]
then
    echo "Downloading files..."
    if [ -d ${DATA_DIR}/*.* ]; then
      rm -v ${DATA_DIR}/*.* || true
    fi
    while read -r line; do
        [[ "$line" =~ ^#.*$ ]] && continue
        wget -c -P ${DATA_DIR}/ "https://yago-knowledge.org/data/yago4/full/2020-02-24/"$line
        if [[ $line == *"yago-wd-labels"* ]]
        then
          echo "Keeping only english labels"
          zcat ${DATA_DIR}/${line##*/} |  grep --color=never  -e "@en\s." | grep  --color=never  -v -f ./exclude.txt > ${DATA_DIR}/yago-wd-labels-en.nt
          rm ${DATA_DIR}/${line##*/}
          filename="yago-wd-labels-en.nt"
        elif [[ $line == *"yago-wd-facts"* ]]
        then
          echo "excluding useless only english labels"
          zcat ${DATA_DIR}/${line##*/} |  grep --color=never  -v -f ./exclude.txt > ${DATA_DIR}/yago-wd-facts-lite.nt
          rm ${DATA_DIR}/${line##*/}
          filename="yago-wd-facts-lite.nt"
        else
          gzip -d ${DATA_DIR}/${line##*/}
          filename=$(basename -- "${DATA_DIR}/${line##*/}")
          filename="${filename%.*}"
        fi
        split -l 500000 --numeric-suffixes ${DATA_DIR}/${filename} ${DATA_DIR}/part-${filename}
        rm ${DATA_DIR}/${filename}
    done < $1
    mv ${DATA_DIR}/part-*.nt* ${NEO4J_IMPORT}/

    chmod -R 777 ${NEO4J_IMPORT}
else
    echo "No destination folder ${DATA_DIR}"
fi
