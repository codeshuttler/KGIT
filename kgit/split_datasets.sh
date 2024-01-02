#!/bin/bash
python rq/split_dataset.py  --input result/baseline/ir1/check_pre_unifiedqa-v2-t5-small-1363200.txt
python rq/split_dataset.py  --input result/baseline/ir2/check_pre_unifiedqa-v2-t5-small-1363200.txt
python rq/split_dataset.py  --input result/baseline/ir3/check_pre_unifiedqa-v2-t5-small-1363200.txt
python rq/split_dataset.py  --input result/baseline/ir4/check_pre_unifiedqa-v2-t5-small-1363200.txt

python rq/split_dataset.py  --input result/baseline/ir1/check_pre_unifiedqa-v2-t5-base-1363200.txt
python rq/split_dataset.py  --input result/baseline/ir2/check_pre_unifiedqa-v2-t5-base-1363200.txt
python rq/split_dataset.py  --input result/baseline/ir3/check_pre_unifiedqa-v2-t5-base-1363200.txt
python rq/split_dataset.py  --input result/baseline/ir4/check_pre_unifiedqa-v2-t5-base-1363200.txt

python rq/split_dataset.py  --input result/baseline/ir1/check_pre_unifiedqa-v2-t5-large-1363200.txt
python rq/split_dataset.py  --input result/baseline/ir2/check_pre_unifiedqa-v2-t5-large-1363200.txt
python rq/split_dataset.py  --input result/baseline/ir3/check_pre_unifiedqa-v2-t5-large-1363200.txt
python rq/split_dataset.py  --input result/baseline/ir4/check_pre_unifiedqa-v2-t5-large-1363200.txt
