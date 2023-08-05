import json
import argparse
import random


def main(filepath: str):
    random.seed(43)
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    indices = list(range(len(lines)))
    random.shuffle(indices)

    train_data = []
    valid_data = []
    test_data = []

    train_index = int(0.6 * len(lines))
    valid_index = int(0.8 * len(lines))

    for i in indices[:train_index]:
        train_data.append(lines[i])
    
    for i in indices[train_index:valid_index]:
        valid_data.append(lines[i])
    
    for i in indices[valid_index:]:
        test_data.append(lines[i])
    
    filename, ext = filepath.rsplit(".", maxsplit=2)
    
    with open(f"{filename}_train.{ext}", "w", encoding="utf-8") as f:
        for line in train_data:
            f.write(line)
    
    with open(f"{filename}_valid.{ext}", "w", encoding="utf-8") as f:
        for line in valid_data:
            f.write(line)
    
    with open(f"{filename}_test.{ext}", "w", encoding="utf-8") as f:
        for line in test_data:
            f.write(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--input", type=str, help="input jsonl data file")
    args = parser.parse_args()
    main(args.input)
