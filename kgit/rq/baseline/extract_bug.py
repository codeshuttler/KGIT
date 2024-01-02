import json
import argparse
import random


def main(filepath: str):
    random.seed(43)
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--input", type=str, help="input jsonl data file")
    args = parser.parse_args()
    main(args.input)