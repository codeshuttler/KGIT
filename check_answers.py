
import argparse
import json
import os
from typing import List
import tqdm
from kgit.utils import chunked
from kgit.check import check_answer

def check(input_path: str, output_path: str, state: str):
    '''
    state: "all", "first"
    '''
    dataset = []
    with open(input_path, "r", encoding="utf-8") as f:
        for line in tqdm.tqdm(f):
            try:
                dataset.append(json.loads(line))
            except:
                break

    # count
    with open(output_path, 'w', encoding='utf-8') as f:
        for qa_pair in tqdm.tqdm(dataset):
            preliminaries = qa_pair["preliminaries"]
            test_case = qa_pair["test"]

            checklist = []
            for pre_qa in preliminaries:
                question = pre_qa["question"]
                answer = pre_qa["answer"]
                if "answer_hat" not in pre_qa:
                    checklist.append(False)
                    continue
                answer_hat = pre_qa["answer_hat"]
                checklist.append(check_answer(answer, answer_hat))
            
            if all(checklist):
                test_checklist = []
                for test_qa in test_case:
                    question = test_qa["question"]
                    answer = test_qa["answer"]
                    answer_hat = test_qa["answer_hat"]
                    test_checklist.append(check_answer(answer, answer_hat))
                
                if state == "all":
                    if not all(test_checklist):
                        f.write(json.dumps(qa_pair) + "\n")
                elif state == "first":
                    if len(test_checklist) > 0 and not test_checklist[0]:
                        f.write(json.dumps(qa_pair) + "\n")
                elif state == "pre":
                    f.write(json.dumps(qa_pair) + "\n")
                else:
                    if not all(test_checklist):
                        f.write(json.dumps(qa_pair) + "\n")
                    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', "--answer", type=str, help="answer file")
    parser.add_argument('-o', '--output', type=str, help='output path')
    parser.add_argument('-s', '--state', type=str, default="all", help='check state')

    args = parser.parse_args()
    
    check(args.answer, args.output, args.state)