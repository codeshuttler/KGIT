import json
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
)

import os.path
import pandas as pd

MODELS = ["unifiedqa-v2-t5-small-1363200", "unifiedqa-v2-t5-base-1363200", "unifiedqa-v2-t5-large-1363200"]
MODELS_SIZE = ["small", "base", "large"]
KRS = ["kr1", "kr2", "kr3", "kr4"]

for kr in KRS:
    for mode in MODELS:
        pass

import os
import pandas as pd
import matplotlib.pyplot as plt
from kbqat import venn
import tqdm
from kbqat.utils import read_dataset

from kbqat.check import check_answer

def is_all_pass(question_list):
    test_checklist = []
    for qa_pair in question_list:
        question = qa_pair["question"]
        answer = qa_pair["answer"]
        answer_hat = qa_pair["answer_hat"]
        test_checklist.append(check_answer(answer, answer_hat))
    return all(test_checklist)


def main():
    fig=plt.figure(figsize=(18,6))
    ax1 = fig.add_subplot(141)
    ax2 = fig.add_subplot(142)
    ax3 = fig.add_subplot(143)

    ax_list = [ax1, ax2, ax3]

    kr_names = ["(a) Small", "(b) Base", "(c) Large"]

    
    for model_i, model in enumerate(MODELS_SIZE):
        print(model)
        labels = {}
    
        qaqa_labels = []
        kgit_labels = []
        for kr_i, kr_name in enumerate(KRS):
            # QAQA output
            qaqa_file = f"/data/wangjun/github/QAQA/results/{kr_name}_{model}/res-dev/{kr_name}_{model}_violation_all.tsv"
            kgit_file = f"result/baseline/{kr_name}/check_pre_unifiedqa-v2-t5-{model}-1363200_test_sampled.jsonl"

            with open(qaqa_file, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.split("\t")
                    idx = int(parts[0])
                    qaqa_labels.append(f"{kr_i}-{idx//2}")
            
            with open(kgit_file, "r", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    data = json.loads(line)
                    preliminaries = data["preliminaries"]
                    test_case = data["test"]
                    for qa_pair in test_case:
                        question = qa_pair["question"]
                        answer = qa_pair["answer"]
                        answer_hat = qa_pair["answer_hat"]
                        if not check_answer(answer, answer_hat):
                            kgit_labels.append(f"{kr_i}-{i}")
        
        labels["QAQA"] = qaqa_labels
        labels["KGIT"] = kgit_labels
    
        labels = venn.get_labels([labels["QAQA"], labels["KGIT"]], fill=['number'])
        ax = venn.venn2_ax(ax_list[model_i], labels, names=['QAQA', 'KGIT'], legend=(model==2), fontsize=11)
        ax.set_title(MODELS[model_i], y=-0.08, fontdict={'fontsize':16})

    fig.savefig(f"rq_result/baseline_venn_out.pdf")
 
    # out_df = pd.DataFrame(out)
    # out_df.to_csv("rq3_2.csv", index=False)

if __name__ == "__main__":
    main()