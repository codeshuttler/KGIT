model_list=("unifiedqa-v2-t5-small-1363200" "unifiedqa-v2-t5-base-1363200" "unifiedqa-v2-t5-large-1363200") # "unifiedqa-v2-t5-3b-1251000"

for model in ${model_list[@]};
do
echo "Answer and check model $model"
python answer_questions.py -q result/ir1/questions.jsonl -o result/ir1/answers_${model}.txt --device cuda --model ${model}
python answer_questions.py -q result/ir2/questions.jsonl -o result/ir2/answers_${model}.txt --device cuda --model ${model}
python answer_questions.py -q result/ir3/questions.jsonl -o result/ir3/answers_${model}.txt --device cuda --model ${model}
python answer_questions.py -q result/ir4/questions.jsonl -o result/ir4/answers_${model}.txt --device cuda --model ${model}

python answer_questions.py -q result/ir1/questions.jsonl -o result/ir1/answers_nc_${model}.txt --device cuda --model ${model} --nocontext
python answer_questions.py -q result/ir2/questions.jsonl -o result/ir2/answers_nc_${model}.txt --device cuda --model ${model} --nocontext
python answer_questions.py -q result/ir3/questions.jsonl -o result/ir3/answers_nc_${model}.txt --device cuda --model ${model} --nocontext
python answer_questions.py -q result/ir4/questions.jsonl -o result/ir4/answers_nc_${model}.txt --device cuda --model ${model} --nocontext

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

python check_questions.py -a result/ir1/answers_nc_${model}.txt -o result/ir1/check_nc_all_${model}.txt -s all
python check_questions.py -a result/ir2/answers_nc_${model}.txt -o result/ir2/check_nc_all_${model}.txt -s all
python check_questions.py -a result/ir3/answers_nc_${model}.txt -o result/ir3/check_nc_all_${model}.txt -s all
python check_questions.py -a result/ir4/answers_nc_${model}.txt -o result/ir4/check_nc_all_${model}.txt -s all

python check_questions.py -a result/ir1/answers_nc_${model}.txt -o result/ir1/check_nc_first_${model}.txt -s first
python check_questions.py -a result/ir2/answers_nc_${model}.txt -o result/ir2/check_nc_first_${model}.txt -s first
python check_questions.py -a result/ir3/answers_nc_${model}.txt -o result/ir3/check_nc_first_${model}.txt -s first
python check_questions.py -a result/ir4/answers_nc_${model}.txt -o result/ir4/check_nc_first_${model}.txt -s first

python check_questions.py -a result/ir1/answers_nc_${model}.txt -o result/ir1/check_nc_pre_${model}.txt -s pre
python check_questions.py -a result/ir2/answers_nc_${model}.txt -o result/ir2/check_nc_pre_${model}.txt -s pre
python check_questions.py -a result/ir3/answers_nc_${model}.txt -o result/ir3/check_nc_pre_${model}.txt -s pre
python check_questions.py -a result/ir4/answers_nc_${model}.txt -o result/ir4/check_nc_pre_${model}.txt -s pre
done
