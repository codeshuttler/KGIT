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
IRS = ["metamorphic1", "metamorphic2", "metamorphic3", "metamorphic4"]

def main():
    for ir_i, ir in enumerate(IRS):
        question_file = f"result/{ir}/questions.txt"
        dataset = read_dataset(question_file)
        print(ir, len(dataset))


if __name__ == "__main__":
    main()


