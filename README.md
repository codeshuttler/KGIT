# KGIT

This is the source code for the paper "Knowledge Graph Driven Inference Testing for Question Answering Software".

## Package Requirement

To run this code, some packages are needed as following:

```python
sentencepiece==0.1.97
transformers==4.24.0
neo4j==5.3.0
neomodel==4.0.8
datasets==2.8.0
faiss-cpu==1.7.3
matplotlib==3.6.3
myers==1.0.1
openpyxl==3.1.0
sentence-transformers==2.2.2
```

All code in this repository is tested under the environment of `Python 3.8.13`.

## Prepare dataset

Due to the license of the original knowledge graph YAGO4, we do not provide download links here, please download from [YAGO4](https://yago-knowledge.org/downloads/yago-4).
Then import the YAGO4 data into neo4j. 

## Generate Test Cases

```python
python ir1.py
python ir2.py
python ir3.py
python ir4.py
```

## Answer Questions

```bash
python answer_questions.py -q result/ir1/questions.txt -o result/ir1/answers_${model}.txt --device cuda:0 --model ${model}
python answer_questions.py -q result/ir2/questions.txt -o result/ir2/answers_${model}.txt --device cuda:0 --model ${model}
python answer_questions.py -q result/ir3/questions.txt -o result/ir3/answers_${model}.txt --device cuda:0 --model ${model}
python answer_questions.py -q result/ir4/questions.txt -o result/ir4/answers_${model}.txt --device cuda:0 --model ${model}
```

## Check Answers

```bash
python check_questions.py -a result/ir1/answers_${model}.txt -o result/ir1/check_all_${model}.txt -s all
python check_questions.py -a result/ir2/answers_${model}.txt -o result/ir2/check_all_${model}.txt -s all
python check_questions.py -a result/ir3/answers_${model}.txt -o result/ir3/check_all_${model}.txt -s all
python check_questions.py -a result/ir4/answers_${model}.txt -o result/ir4/check_all_${model}.txt -s all

python check_questions.py -a result/ir1/answers_${model}.txt -o result/ir1/check_first_${model}.txt -s first
python check_questions.py -a result/ir2/answers_${model}.txt -o result/ir2/check_first_${model}.txt -s first
python check_questions.py -a result/ir3/answers_${model}.txt -o result/ir3/check_first_${model}.txt -s first
python check_questions.py -a result/ir4/answers_${model}.txt -o result/ir4/check_first_${model}.txt -s first

python check_questions.py -a result/ir1/answers_${model}.txt -o result/ir1/check_pre_${model}.txt -s pre
python check_questions.py -a result/ir2/answers_${model}.txt -o result/ir2/check_pre_${model}.txt -s pre
python check_questions.py -a result/ir3/answers_${model}.txt -o result/ir3/check_pre_${model}.txt -s pre
python check_questions.py -a result/ir4/answers_${model}.txt -o result/ir4/check_pre_${model}.txt -s pre
```

## RQs

```bash
# RQ1
python rq/manual_check_sample.py
# Manual Check and get statistics
python rq/manual_check_summary.py

# RQ2
python rq/effectiveness_all.py
python rq/effectiveness_first.py

# RQ3
python rq/retrain.py --unifiedqa_path allenai/unifiedqa-v2-t5-small-1363200 --model_type small --subtask ir1 --start_step 1363200 --batch 64
python rq/retrain.py --unifiedqa_path allenai/unifiedqa-v2-t5-base-1363200 --model_type base --subtask ir1 --start_step 1363200 --batch 64
python rq/retrain.py --unifiedqa_path allenai/unifiedqa-v2-t5-large-1363200 --model_type large --subtask ir1 --start_step 1363200 --batch 64

python rq/retrain.py --unifiedqa_path allenai/unifiedqa-v2-t5-small-1363200 --model_type small --subtask ir2 --start_step 1363200 --batch 64
python rq/retrain.py --unifiedqa_path allenai/unifiedqa-v2-t5-base-1363200 --model_type base --subtask ir2 --start_step 1363200 --batch 64
python rq/retrain.py --unifiedqa_path allenai/unifiedqa-v2-t5-large-1363200 --model_type large --subtask ir2 --start_step 1363200 --batch 64

python rq/retrain.py --unifiedqa_path allenai/unifiedqa-v2-t5-small-1363200 --model_type small --subtask ir3 --start_step 1363200 --batch 64
python rq/retrain.py --unifiedqa_path allenai/unifiedqa-v2-t5-base-1363200 --model_type base --subtask ir3 --start_step 1363200 --batch 64
python rq/retrain.py --unifiedqa_path allenai/unifiedqa-v2-t5-large-1363200 --model_type large --subtask ir3 --start_step 1363200 --batch 64

python rq/retrain.py --unifiedqa_path allenai/unifiedqa-v2-t5-small-1363200 --model_type small --subtask ir4 --start_step 1363200 --batch 64
python rq/retrain.py --unifiedqa_path allenai/unifiedqa-v2-t5-base-1363200 --model_type base --subtask ir4 --start_step 1363200 --batch 64
python rq/retrain.py --unifiedqa_path allenai/unifiedqa-v2-t5-large-1363200 --model_type large --subtask ir4 --start_step 1363200 --batch 64

# RQ4
# Here we get the train/valid/test dataset under folder ./result/baseline/ for QAQA
bash setup_baseline_data.sh
# Then prepare the code and environment of QAQA following the readme in QAQA repo: https://github.com/ShenQingchao/QAQA.git
pushd ../
git clone https://github.com/ShenQingchao/QAQA.git
popd
# Please install the QAQA and setup configs following the readme https://github.com/ShenQingchao/QAQA/blob/master/README.md

# discussion
python rq/effectiveness_all_nc.py
python rq/effectiveness_first_nc.py
python rq/efficiency.py
python rq/overlaps.py
python rq/scale.py
```

## Relation List

In YAGO4, relations and attributes come from [schema.org](schema.org), and all relations have the prefix 'sch__'.
In the paper, for brevity, we ignore all the prefix 'sch_'.

IR1:

| R1              | R1 Extension      | R2                | R2 Extension         |
| --------------- | ----------------- | ----------------- | -------------------- |
| sch__author     | the author of     | sch__affiliation  | the affiliation of   |
| sch__creator    | the creator of    | sch__alumniOf     | an alumnus of        |
| sch__colorist   | the colorist of   | sch__birthPlace   | the birthplace of    |
| sch__composer   | the composer of   | sch__children     | a child of           |
| sch__director   | the director of   | sch__deathPlace   | the death place of   |
| sch__editor     | the editor of     | sch__familyName   | the family name of   |
| sch__founder    | the founder of    | sch__givenName    | the given name of    |
| sch__organizer  | the organizer of  | sch__gender       | the gender of        |
| sch__publisher  | the publisher of  | sch__homeLocation | the home location of |
| sch__provider   | the provider of   | sch__location     | the location of      |
| sch__producer   | the producer of   | sch__parent       | a parent of          |
| sch__translator | the translator of |                   |                      |
|                 |                   |                   |                      |

IR2:

| R                 | R Extension         |
| ----------------- | ------------------- |
| sch__actor        | an actor in         |
| sch__affiliation  | the affiliation of  |
| sch__alumniOf     | an alumnus of       |
| sch__author       | the author of       |
| sch__birthPlace   | the birthplace of   |
| sch__brand        | the brand of        |
| sch__character    | a character in      |
| sch__children     | a child of          |
| sch__colorist     | the colorist of     |
| sch__competitor   | a competitor of     |
| sch__composer     | the composer of     |
| sch__deathPlace   | the death place of  |
| sch__editor       | the editor of       |
| sch__familyName   | the family name of  |
| sch__givenName    | the given name of   |
| sch__gender       | the gender of       |
| sch__homeLocation | the homeLocation of |
| sch__organizer    | the organizer of    |
| sch__creator      | the creator of      |
| sch__location     | the location of     |
| sch__parent       | a parent of         |
| sch__director     | the director of     |
| sch__founder      | the founder of      |
| sch__producer     | the producer of     |
| sch__provider     | the provider of     |
| sch__publisher    | the publisher of    |
| sch__sponsor      | a sponsor of        |
| sch__translator   | the translator of   |

R3:

| R                  | R Extension |
| ------------------ | ----------- |
| sch__hasPart       | a part of   |
| sch__containsPlace | a place in  |

R4:

| R               |   R Extension     |
| --------------- | ----------------- |
| sch__hasPart    | a part of         |
| sch__parent     | a parent of       |
| sch__children   | a child of        |
| sch__author     | the author of     |
| sch__editor     | the editor of     |
| sch__creator    | the creator of    |
| sch__organizer  | the organizer of  |
| sch__director   | the director of   |
| sch__founder    | the founder of    |
| sch__producer   | the producer of   |
| sch__provider   | the provider of   |
| sch__publisher  | the publisher of  |
| sch__sponsor    | a sponsor of      |
| sch__translator | the translator of |
| sch__colorist   | the colorist of   |
| sch__competitor | a competitor of   |
| sch__composer   | the composer of   |

# References

For more details about data processing, please refer to the `code comments` and our paper.