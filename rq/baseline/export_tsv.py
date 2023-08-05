
import random
import json
import csv
import argparse


def export_tsv(file: str):
    random.seed(43)
    print(file)
    samples = []
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            samples.append(json.loads(line))
    
    if len(samples) > 10000:
        samples = random.sample(samples, 10000)

    filename, ext = file.rsplit(".", maxsplit=2)
    with open(f"{filename}_sampled.jsonl", "w", encoding="utf-8") as f:
        for sample in samples:
            f.write(json.dumps(sample) + '\n')

    out_samples = []
    for sample in samples:
        tests = sample["test"]
        
        for test in tests:
            out_samples.append((test["question"], test["answer"], test["context"]))
    
    filename, ext = file.rsplit(".", maxsplit=2)

    with open(f'{filename}.tsv', 'w', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
        
        for record in out_samples:
            writer.writerow([f"{record[0]} \\n {record[2]}", record[1]])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--input", type=str, help="input jsonl data file")
    args = parser.parse_args()
    export_tsv(args.input)
