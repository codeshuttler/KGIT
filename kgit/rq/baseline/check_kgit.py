import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
)

import json
import pandas as pd

from kbqat.check import check_answer

def is_all_pass(question_list):
    test_checklist = []
    for qa_pair in question_list:
        question = qa_pair["question"]
        answer = qa_pair["answer"]
        answer_hat = qa_pair["answer_hat"]
        test_checklist.append(check_answer(answer, answer_hat))
    return all(test_checklist)

data_frame = {
    "kr": [],
    "model": [],
    "number": [],
    "bug_count": []
}
KR_LIST = ["kr1", "kr2", "kr3", "kr4"]
MODEL_LIST = ["unifiedqa-v2-t5-small-1363200", "unifiedqa-v2-t5-base-1363200", "unifiedqa-v2-t5-large-1363200"]
for kr in KR_LIST:
    for model in MODEL_LIST:
        path = f"result/baseline/{kr}/check_pre_{model}_test_sampled.jsonl"
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        data_frame["kr"].append(kr)
        data_frame["model"].append(model)
        data_frame["number"].append(len(lines))

        bug_count = 0
        for line in lines:
            data = json.loads(line)
            preliminaries = data["preliminaries"]
            test_case = data["test"]
            if not is_all_pass(test_case):
                bug_count += 1
        data_frame["bug_count"].append(bug_count)
        print(kr, model, len(lines), bug_count)

pd.DataFrame(data_frame).to_csv("volation_kgit.csv")
