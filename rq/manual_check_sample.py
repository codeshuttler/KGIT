import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
)

import os
import random
from kgit.utils import read_dataset, write_dataset
import pandas as pd

SAMPLE_NUM = 100
MODELS = ["unifiedqa-v2-t5-small-1363200", "unifiedqa-v2-t5-base-1363200", "unifiedqa-v2-t5-large-1363200"]
KRS = ["ir1", "ir2", "ir3", "ir4"]

def main(data_path: str, out_path: str):
    random.seed(43)
    for kr in KRS:
        kr_dir = os.path.join(data_path, kr)
        question_file = os.path.join(kr_dir, "questions.txt")
        data = read_dataset(question_file)
        sampled_data = random.sample(data, 100)

        out_file = os.path.join(out_path, kr + "_sample.xlsx")
        dataframe = {
            "id": [],
            "question": [],
            "answer": [],
            "group": [],
            "error": []
        }
        for i, item in enumerate(sampled_data):
            preliminaries = item["preliminaries"]
            test_case = item["test"]
            for qa_pair in preliminaries:
                dataframe["id"].append(i)
                dataframe["question"].append(qa_pair["question"])
                dataframe["answer"].append(qa_pair["answer"])
                dataframe["group"].append(0)
                dataframe["error"].append(0)
            
            for qa_pair in test_case:
                dataframe["id"].append(i)
                dataframe["question"].append(qa_pair["question"])
                dataframe["answer"].append(qa_pair["answer"])
                dataframe["group"].append(1)
                dataframe["error"].append(0)
        
        df = pd.DataFrame(dataframe)
        df.to_excel(out_file)

if __name__ == "__main__":
    main('./result', './rq_result/manual_check')