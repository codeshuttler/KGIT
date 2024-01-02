import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
)

import os.path
import pandas as pd

MODELS = ["unifiedqa-v2-t5-small-1363200", "unifiedqa-v2-t5-base-1363200", "unifiedqa-v2-t5-large-1363200"]
IRS = ["ir1", "ir2", "ir3", "ir4"]

for ir in IRS:
    for mode in MODELS:
        pass

import os
import pandas as pd
import matplotlib.pyplot as plt
from kgit import venn
import tqdm
from kgit.utils import read_dataset

def main():
    fig=plt.figure(figsize=(24,6))
    ax1 = fig.add_subplot(141)
    ax2 = fig.add_subplot(142)
    ax3 = fig.add_subplot(143)
    ax4 = fig.add_subplot(144)

    ax_list = [ax1, ax2, ax3, ax4]

    ir_names = ["(a) IR1", "(b) IR2", "(c) IR3", "(d) IR4"]

    for ir_i, ir_name in enumerate(IRS):
        labels = {}
        for m in MODELS:
            labels[m] = []

        for model in MODELS:
            print(ir_name, model)
            path = f"result/{ir_name}/check_all_{model}.txt"
            dataset = read_dataset(path)
            for data in dataset:
                test = data["test"]
                id_str = "".join([test_qa["question"] for test_qa in test])
                labels[model].append(id_str)
        labels = venn.get_labels([labels["unifiedqa-v2-t5-small-1363200"], labels["unifiedqa-v2-t5-base-1363200"], labels["unifiedqa-v2-t5-large-1363200"]], fill=['number'])
        ax = venn.venn3_ax(ax_list[ir_i], labels, names=['small', 'base', 'large'], legend=(ir_i==3), fontsize=11)
        ax.set_title(ir_names[ir_i], y=-0.08, fontdict={'fontsize':16})

    fig.savefig(f"rq_result/venn_out.pdf")
 
    # out_df = pd.DataFrame(out)
    # out_df.to_csv("rq3_2.csv", index=False)

if __name__ == "__main__":
    main()