from collections import defaultdict
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

def main():
    random.seed(43)
    for kr in KRS:
        mark_file = f"./rq_result/manual_check/{kr}_sample_marked.xlsx"
        if not os.path.exists(mark_file):
            continue
        df = pd.read_excel(mark_file)

        data = defaultdict(list)
        for i, row in df.iterrows():
            data[row['id']].append(row['error'])
        
        grammar_error = 0
        fact_error = 0
        for k, v in data.items():
            if any([item == 1 for item in v]):
                grammar_error += 1
            if any([item == 2 for item in v]):
                fact_error += 1
        
        print(kr, grammar_error, fact_error)


if __name__ == "__main__":
    main()