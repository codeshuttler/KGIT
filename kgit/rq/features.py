

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
KRS = ["kr1", "kr2", "kr3", "kr4"]

def main():
    for model_i, model in enumerate(MODELS):
        for kr_i, kr in enumerate(KRS):
            print(model, kr)
            check_file = f"result/{kr}/check_all_{model}.txt"
            all_correct_dataset = read_dataset(check_file)



if __name__ == "__main__":
    main()

