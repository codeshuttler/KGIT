
cp result/ir1/check_pre_unifiedqa-v2-t5-small-1363200.txt result/baseline/ir1/check_pre_unifiedqa-v2-t5-small-1363200.txt
cp result/ir2/check_pre_unifiedqa-v2-t5-small-1363200.txt result/baseline/ir2/check_pre_unifiedqa-v2-t5-small-1363200.txt
cp result/ir3/check_pre_unifiedqa-v2-t5-small-1363200.txt result/baseline/ir3/check_pre_unifiedqa-v2-t5-small-1363200.txt
cp result/ir4/check_pre_unifiedqa-v2-t5-small-1363200.txt result/baseline/ir4/check_pre_unifiedqa-v2-t5-small-1363200.txt

cp result/ir1/check_pre_unifiedqa-v2-t5-base-1363200.txt result/baseline/ir1/check_pre_unifiedqa-v2-t5-base-1363200.txt
cp result/ir2/check_pre_unifiedqa-v2-t5-base-1363200.txt result/baseline/ir2/check_pre_unifiedqa-v2-t5-base-1363200.txt
cp result/ir3/check_pre_unifiedqa-v2-t5-base-1363200.txt result/baseline/ir3/check_pre_unifiedqa-v2-t5-base-1363200.txt
cp result/ir4/check_pre_unifiedqa-v2-t5-base-1363200.txt result/baseline/ir4/check_pre_unifiedqa-v2-t5-base-1363200.txt

cp result/ir1/check_pre_unifiedqa-v2-t5-large-1363200.txt result/baseline/ir1/check_pre_unifiedqa-v2-t5-large-1363200.txt
cp result/ir2/check_pre_unifiedqa-v2-t5-large-1363200.txt result/baseline/ir2/check_pre_unifiedqa-v2-t5-large-1363200.txt
cp result/ir3/check_pre_unifiedqa-v2-t5-large-1363200.txt result/baseline/ir3/check_pre_unifiedqa-v2-t5-large-1363200.txt
cp result/ir4/check_pre_unifiedqa-v2-t5-large-1363200.txt result/baseline/ir4/check_pre_unifiedqa-v2-t5-large-1363200.txt

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


# small
python rq/baseline/export_tsv.py --input result/baseline/ir1/check_pre_unifiedqa-v2-t5-small-1363200_train.txt
python rq/baseline/export_tsv.py --input result/baseline/ir1/check_pre_unifiedqa-v2-t5-small-1363200_valid.txt
python rq/baseline/export_tsv.py --input result/baseline/ir1/check_pre_unifiedqa-v2-t5-small-1363200_test.txt

python rq/baseline/export_tsv.py --input result/baseline/ir2/check_pre_unifiedqa-v2-t5-small-1363200_train.txt
python rq/baseline/export_tsv.py --input result/baseline/ir2/check_pre_unifiedqa-v2-t5-small-1363200_valid.txt
python rq/baseline/export_tsv.py --input result/baseline/ir2/check_pre_unifiedqa-v2-t5-small-1363200_test.txt

python rq/baseline/export_tsv.py --input result/baseline/ir3/check_pre_unifiedqa-v2-t5-small-1363200_train.txt
python rq/baseline/export_tsv.py --input result/baseline/ir3/check_pre_unifiedqa-v2-t5-small-1363200_valid.txt
python rq/baseline/export_tsv.py --input result/baseline/ir3/check_pre_unifiedqa-v2-t5-small-1363200_test.txt

python rq/baseline/export_tsv.py --input result/baseline/ir4/check_pre_unifiedqa-v2-t5-small-1363200_train.txt
python rq/baseline/export_tsv.py --input result/baseline/ir4/check_pre_unifiedqa-v2-t5-small-1363200_valid.txt
python rq/baseline/export_tsv.py --input result/baseline/ir4/check_pre_unifiedqa-v2-t5-small-1363200_test.txt


# base
python rq/baseline/export_tsv.py --input result/baseline/ir1/check_pre_unifiedqa-v2-t5-base-1363200_train.txt
python rq/baseline/export_tsv.py --input result/baseline/ir1/check_pre_unifiedqa-v2-t5-base-1363200_valid.txt
python rq/baseline/export_tsv.py --input result/baseline/ir1/check_pre_unifiedqa-v2-t5-base-1363200_test.txt

python rq/baseline/export_tsv.py --input result/baseline/ir2/check_pre_unifiedqa-v2-t5-base-1363200_train.txt
python rq/baseline/export_tsv.py --input result/baseline/ir2/check_pre_unifiedqa-v2-t5-base-1363200_valid.txt
python rq/baseline/export_tsv.py --input result/baseline/ir2/check_pre_unifiedqa-v2-t5-base-1363200_test.txt

python rq/baseline/export_tsv.py --input result/baseline/ir3/check_pre_unifiedqa-v2-t5-base-1363200_train.txt
python rq/baseline/export_tsv.py --input result/baseline/ir3/check_pre_unifiedqa-v2-t5-base-1363200_valid.txt
python rq/baseline/export_tsv.py --input result/baseline/ir3/check_pre_unifiedqa-v2-t5-base-1363200_test.txt

python rq/baseline/export_tsv.py --input result/baseline/ir4/check_pre_unifiedqa-v2-t5-base-1363200_train.txt
python rq/baseline/export_tsv.py --input result/baseline/ir4/check_pre_unifiedqa-v2-t5-base-1363200_valid.txt
python rq/baseline/export_tsv.py --input result/baseline/ir4/check_pre_unifiedqa-v2-t5-base-1363200_test.txt

# large
python rq/baseline/export_tsv.py --input result/baseline/ir1/check_pre_unifiedqa-v2-t5-large-1363200_train.txt
python rq/baseline/export_tsv.py --input result/baseline/ir1/check_pre_unifiedqa-v2-t5-large-1363200_valid.txt
python rq/baseline/export_tsv.py --input result/baseline/ir1/check_pre_unifiedqa-v2-t5-large-1363200_test.txt

python rq/baseline/export_tsv.py --input result/baseline/ir2/check_pre_unifiedqa-v2-t5-large-1363200_train.txt
python rq/baseline/export_tsv.py --input result/baseline/ir2/check_pre_unifiedqa-v2-t5-large-1363200_valid.txt
python rq/baseline/export_tsv.py --input result/baseline/ir2/check_pre_unifiedqa-v2-t5-large-1363200_test.txt

python rq/baseline/export_tsv.py --input result/baseline/ir3/check_pre_unifiedqa-v2-t5-large-1363200_train.txt
python rq/baseline/export_tsv.py --input result/baseline/ir3/check_pre_unifiedqa-v2-t5-large-1363200_valid.txt
python rq/baseline/export_tsv.py --input result/baseline/ir3/check_pre_unifiedqa-v2-t5-large-1363200_test.txt

python rq/baseline/export_tsv.py --input result/baseline/ir4/check_pre_unifiedqa-v2-t5-large-1363200_train.txt
python rq/baseline/export_tsv.py --input result/baseline/ir4/check_pre_unifiedqa-v2-t5-large-1363200_valid.txt
python rq/baseline/export_tsv.py --input result/baseline/ir4/check_pre_unifiedqa-v2-t5-large-1363200_test.txt
