
'''
本文数据规模
'''
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
)

from kgit.utils import read_dataset

MODELS = ["unifiedqa-v2-t5-small-1363200", "unifiedqa-v2-t5-base-1363200", "unifiedqa-v2-t5-large-1363200"]
KRS = ["ir1", "ir2", "ir3", "ir4"]

def main():
    for kr_i, kr in enumerate(KRS):
        entities = set()
        counter = 0
        dataset = read_dataset(f"result/{kr}/questions.txt")
        for data in dataset:
            a = data["a_id"]
            entities.add(a)
            b = data["b_id"]
            entities.add(b)
            if kr_i not in [1,3]:
                c = data["c_id"]
                entities.add(c)

            counter += 1
        print(kr, counter, len(entities))

if __name__ == "__main__":
    main()