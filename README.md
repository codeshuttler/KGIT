# KGIT

## Purpose
To generate the questions with the inference relations automatically, we propose a novel testing method Knowledge Graph driven Inference Testing (***KGIT***), which employs facts in the Knowledge Graph (KG) as the seeds to logically construct test cases containing questions and contexts with inference relations.

The artifact contains two parts.
The first part stores YAGO4 knowledge graph data into a Neo4j graph database.
The second part queries Neo4j for entity relationship pairs that meet certain conditions and generating test cases.
Finally, the data is input into question-answering models to obtain results.

## Badges
We are applying for the following badges:
- Available: we archived the reproducible code on Software Heritage, ensuring long-term availability and accessibility for researchers and practitioners.
- Reusable: we provided information regarding the hardware and software requirements necessary for replication, as well as detailed steps to reproduce the results presented in the paper. By providing clear instructions, we aim to enable other researchers to easily reuse our artifact and build upon our work.

## Provenance
This is the source code for the paper "Knowledge Graph Driven Inference Testing for Question Answering Software".
The artifacts of this paper have already been archived on Software Heritage.
You can download the artifacts of this paper from [HERE](https://archive.softwareheritage.org/browse/origin/https://github.com/codeshuttler/KGIT).

# Data
The data for the artifact is from [YAGO 4](https://yago-knowledge.org/downloads/yago-4). YAGO 4, a version of the YAGO knowledge base that is based on Wikidata — the largest public general-purpose knowledge base. 

We have included a script in our code that downloads the YAGO4 data. However, due to potential slow download speeds from the official YAGO mirror, you can download the data from alternative sources and place it in the `neo4j_server/yago4_data`` directory.

YAGO4 includes the following data files:
* stats.tsv
* yago-wd-full-types.nt.gz
* yago-wd-sameAs.nt.gz
* yago-wd-schema.nt.gz
* yago-wd-shapes.nt.gz
* yago-wd-simple-types.nt.gz

Downloading and deploying the complete YAGO 4 dataset may take a very long time (it took us three days to download and around four hours to import on our own server). Therefore, you can [download](https://github.com/codeshuttler/KGIT/releases/tag/20240102) the generated test cases from our knowledge graph to skip this step.

In addition, we use the question-answering model `unifiedqa-v2-t5`, grammar correction model `pszemraj/flan-t5-large-grammar-synthesis` and text similarity model `sentence-transformers/all-mpnet-base-v2`, and the script automatically downloads the model weights from Hugging Face to the local environment. If the download speed is slow, you can use a Hugging Face mirror or specify the model directory in the code to use a locally downloaded model.

# Setup
## Hardware
Hardware Requirements.

Minimum:
```
Requires a 64-bit processor and operating system.
Operating System: Linux distributions.
Processor: Intel Core i5-6600.
Memory: 64 GB RAM.
GPU: NVIDIA GeForce RTX 2080ti. (GPUs are used for neural network inference, requires at least 6GB of graphics memory. If you run neural networks on the CPU, it may take a significant amount of time.)
Network: Broadband internet connection.
Storage: Requires 128 GB of available space.
```

Tested Hardware:
```
CPU: two slots of 16 Core Intel Xeon Gold 6226R CPU 2.90GHz Processor
Memory: 8x32GB DDR4 DIMM 2933MHz Memory
GPUs: GeForce RTX 3090 GPU.
```

```
CPU: two slots of 32 Core AMD EPYC 7601 32-Core Processor
Memory: 8x32GB DDR4 DIMM 2400MHz Memory
GPUs: GeForce RTX 3090 GPU.
```

## Software

Tested System:
* 64-bit Ubuntu 22.10 with Linux kernel 5.19.0
* 64-bit Ubuntu 22.04.2 LTS Linux kernel 6.2.0

Software Requirements:
* docker-24.0.7
* docker-compose-2.23.3-1
* Anaconda3-2023.09-0-Linux-x86_64 (or Miniconda)

Python Requirements:
* sentencepiece==0.1.97
* transformers==4.24.0
* neo4j==5.8.0
* neomodel==4.0.8
* datasets==2.8.0
* matplotlib==3.6.3
* myers==1.0.1
* sentence-transformers==2.2.2
* openpyxl==3.1.2

All code in this repository is tested under the environment of `Python 3.8.13`. We use conda to construct a virtual environment to run the python program.

## Setup Neo4j (Optional)
The complete YAGO4 dataset occupies approximately 60GB of storage. Downloading and importing it into Neo4j, as well as extracting questions, may require a significant amount of time. Therefore, we provide our generated test cases extracted from KG for [download](https://github.com/codeshuttler/KGIT/releases/tag/20240102).
We packaged the Neo4j database with Docker:
```
bash setup_neo4j.sh
```

## Setup Python Environment
This step requires Conda installation.
```bash
pushd kgit
conda create --prefix=kgitenv python=3.8.13 --yes
eval "$(conda shell.bash hook)"
conda init
conda activate ./kgitenv
pip install -r requirements.txt
popd
```
or
```
bash setup_python.sh
```

# Usage
All the following commands should be executed in the `kgit` directory. Please run `cd kgit` first.
```
├── clean_all.sh
├── docker-compose.yml
├── kgit      <----------------------------HERE
│   ├── answer_check.sh
│   ├── answer_questions.py
│   ├── check_questions.py
│   ├── config.json
│   ├── construct_questions.sh
│   ├── Dockerfile
│   ├── ir1.py
│   ├── ir2.py
│   ├── ir3.py
│   ├── ir4.py
│   ├── kgit
│   ├── kgitenv
│   ├── manual_check
│   ├── requirements.txt
│   ├── result
│   ├── rq
│   └── run.sh
├── LICENSE
├── neo4j_server
│   ├── data
│   ├── Dockerfile
│   ├── download-yago4.sh
│   ├── exclude.txt
│   ├── import-yago4.sh
│   ├── init-pipeline.sh
│   ├── init-rdf.sh
│   ├── logs
│   ├── yago4
│   ├── yago4_data
│   └── yago4_files.txt
├── README.md
├── setup_neo4j.sh
└── setup_python.sh
```

## Generate Test Cases (Optional, need neo4j and YAGO4)
```bash
python ir1.py
python ir2.py
python ir3.py
python ir4.py
```

or

```bash
bash construct_questions.sh
```

If you have downloaded the test cases generated by us, please unzip them and place them in the directory `kgit/result`.

## Answer Questions and Check Answers

```bash
bash answer_check.sh
```
The outputs of all models will be saved in the directory `kgit/result`.

## RQs
RQ1: manual check
```bash
# RQ1
# python rq/manual_check_sample.py
# Manual Check and get statistics
python rq/manual_check_summary.py
```
Then the manual check results will be printed in the terminal.

RQ2: Effectiveness
```bash
# RQ2
# Output: rq_result/effectiveness_all.xlsx
python rq/effectiveness_all.py
# Output: rq_result/effectiveness_first.xlsx
python rq/effectiveness_first.py
```
Then the results will be saved under `kgit/rq_result`.

RQ3: Retrain
We fork the code of [T5](https://github.com/google-research/text-to-text-transfer-transformer) and implement the finetune script.
The finetuning scripts can be found in the [repository](https://github.com/jstzwj/kgit-text-to-text-transfer-transformer).

First, we split the dataset into train, valid and test sets.
```bash
bash copy_to_baselines.sh
bash split_datasets.sh
```

Second, we need to convert the txt data into tsv format.
```bash
bash export_tsv.sh
```

Then copy these tsv to `text-to-text-transfer-transformer`. There are a script named `finetune.py` under the repo.
```bash
# RQ3
python finetune.py --unifiedqa_path allenai/unifiedqa-v2-t5-small-1363200 --model_type small --subtask ir1 --start_step 1363200 --batch 64
python finetune.py --unifiedqa_path allenai/unifiedqa-v2-t5-base-1363200 --model_type base --subtask ir1 --start_step 1363200 --batch 64
python finetune.py --unifiedqa_path allenai/unifiedqa-v2-t5-large-1363200 --model_type large --subtask ir1 --start_step 1363200 --batch 64

python finetune.py --unifiedqa_path allenai/unifiedqa-v2-t5-small-1363200 --model_type small --subtask ir2 --start_step 1363200 --batch 64
python finetune.py --unifiedqa_path allenai/unifiedqa-v2-t5-base-1363200 --model_type base --subtask ir2 --start_step 1363200 --batch 64
python finetune.py --unifiedqa_path allenai/unifiedqa-v2-t5-large-1363200 --model_type large --subtask ir2 --start_step 1363200 --batch 64

python finetune.py --unifiedqa_path allenai/unifiedqa-v2-t5-small-1363200 --model_type small --subtask ir3 --start_step 1363200 --batch 64
python finetune.py --unifiedqa_path allenai/unifiedqa-v2-t5-base-1363200 --model_type base --subtask ir3 --start_step 1363200 --batch 64
python finetune.py --unifiedqa_path allenai/unifiedqa-v2-t5-large-1363200 --model_type large --subtask ir3 --start_step 1363200 --batch 64

python finetune.py --unifiedqa_path allenai/unifiedqa-v2-t5-small-1363200 --model_type small --subtask ir4 --start_step 1363200 --batch 64
python finetune.py --unifiedqa_path allenai/unifiedqa-v2-t5-base-1363200 --model_type base --subtask ir4 --start_step 1363200 --batch 64
python finetune.py --unifiedqa_path allenai/unifiedqa-v2-t5-large-1363200 --model_type large --subtask ir4 --start_step 1363200 --batch 64
```

RQ4: Baselines
In RQ3, we have got the train/valid/test dataset under folder ./result/baseline/ for QAQA.
For more information of QAQA, please reference the repository of [QAQA](https://github.com/ShenQingchao/QAQA.git).
```bash
# RQ4
# In RQ3, we get the train/valid/test dataset under folder ./result/baseline/ for QAQA
# Then prepare the code and environment of QAQA following the readme in QAQA repo: https://github.com/ShenQingchao/QAQA.git
pushd ../
git clone https://github.com/ShenQingchao/QAQA.git
popd
# Please install the QAQA and setup configs following the readme https://github.com/ShenQingchao/QAQA/blob/master/README.md
```

Discussion:
```bash
# discussion
# Output: rq_result/effectiveness_all_nc.xlsx
python rq/effectiveness_all_nc.py
# Output: rq_result/effectiveness_first_nc.xlsx
python rq/effectiveness_first_nc.py

# Output: rq_result/venn_out.pdf
python rq/overlaps.py
```

# LICENSE
Apache License Version 2.0