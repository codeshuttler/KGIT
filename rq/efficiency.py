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
KRS = ["ir1", "ir2", "ir3", "ir4"]

def main():
    for kr_i, kr in enumerate(KRS):
        question_file = f"result/{kr}/questions.txt"
        dataset = read_dataset(question_file)
        print(kr, len(dataset))


if __name__ == "__main__":
    main()


