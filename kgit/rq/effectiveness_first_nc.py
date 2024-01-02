import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
)

import os.path
import pandas as pd

from kgit.check import check_answer
from kgit.utils import read_dataset, write_dataset


MODELS = ["unifiedqa-v2-t5-small-1363200", "unifiedqa-v2-t5-base-1363200", "unifiedqa-v2-t5-large-1363200"]
IRS = ["ir1", "ir2", "ir3", "ir4"]

def is_all_pass(question_list):
    test_checklist = []
    for qa_pair in question_list:
        question = qa_pair["question"]
        answer = qa_pair["answer"]
        answer_hat = qa_pair["answer_hat"]
        test_checklist.append(check_answer(answer, answer_hat))
    return all(test_checklist)

def main():
    dataframe_data = {
        "model": [],
        "ir1_bug": [],
        "ir1_total": [],
        "ir2_bug": [],
        "ir2_total": [],
        "ir3_bug": [],
        "ir3_total": [],
        "ir4_bug": [],
        "ir4_total": [],
    }
    for model_i, model in enumerate(MODELS):
        dataframe_data["model"].append(model)
        for ir_i, ir in enumerate(IRS):
            print(model, ir)
            check_file = f"result/{ir}/check_nc_first_{model}.txt"
            if not os.path.exists(check_file):
                dataframe_data[f"ir{ir_i + 1}_bug"].append(0)
                dataframe_data[f"ir{ir_i + 1}_total"].append(0)
                continue
            with open(check_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            dataframe_data[f"ir{ir_i + 1}_bug"].append(len(lines))

            answer_file = f"result/{ir}/answers_nc_{model}.txt"
            answers = read_dataset(answer_file)

            pre_pass_count = 0
            for answer in answers:
                preliminaries = answer["preliminaries"]
                test_case = answer["test"]

                if is_all_pass(preliminaries):
                    pre_pass_count += 1
            dataframe_data[f"ir{ir_i + 1}_total"].append(pre_pass_count)
    
    df = pd.DataFrame(dataframe_data)
    df.to_excel("rq_result/effectiveness_first_nc.xlsx")

if __name__ == "__main__":
    main()



