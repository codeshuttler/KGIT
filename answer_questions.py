import argparse
import json
import os
from typing import List, Tuple, Union
import tqdm

from kgit.qa_models.albert import Albert
from kgit.qa_models.rag import RAG
from kgit.qa_models.unifiedqa import UnifiedQA

from kgit.utils import chunked

from transformers import pipeline

qa_cache = {}

def save_dataset(path: str, dataset):
    with open(path, "w", encoding="utf-8") as f:
        for line in dataset:
            f.write(json.dumps(line) + '\n')

def run_qa(model, question: Union[str, List[str], List[Tuple[str]]]) -> Union[str, List[str]]:
    global qa_cache

    questions = []
    if isinstance(question, str):
        questions.append(question)
    elif isinstance(question, Tuple):
        questions.append(question)
    else:
        questions = question

    answers = [None] * len(questions)
    no_answer_questions_ids = []

    for i, q in enumerate(questions):
        if q in qa_cache:
            answers[i] = qa_cache[q]
        else:
            no_answer_questions_ids.append(i)

    if len(no_answer_questions_ids) != 0:
        no_answer_questions = [questions[i] for i in no_answer_questions_ids]

        question_param, context_param= zip(*no_answer_questions)
        question_param = list(question_param)
        context_param = list(context_param)
        no_answer_questions_answers = model.run_model_batch(question_param, context_param)
        for i, idx in enumerate(no_answer_questions_ids):
            answers[idx] = no_answer_questions_answers[i]
            qa_cache[questions[idx]] = answers[idx]

    if len(answers) == 1:
        return answers[0]
    else:
        return answers

def test(input_path: str, output_path: str, model, device, use_context=True):
    if use_context:
        print("using context")
    else:
        print("no context")
    if os.path.exists(output_path):
        read_path = output_path
    else:
        read_path = input_path

    dataset = []
    with open(read_path, "r", encoding="utf-8") as f:
        for line in tqdm.tqdm(f):
            dataset.append(json.loads(line))
    # count
    chunk_size = 4
    for i, batch in enumerate(tqdm.tqdm(chunked(dataset, chunk_size), total=len(dataset)//chunk_size)):

        all_questions = []
        for qa_pair in batch:
            preliminaries = qa_pair["preliminaries"]
            test_case = qa_pair["test"]

            if use_context:
                all_questions.extend([(pre_qa["question"], pre_qa["context"]) for pre_qa in preliminaries if "answer_hat" not in pre_qa])
                all_questions.extend([(test_qa["question"], test_qa["context"]) for test_qa in test_case if "answer_hat" not in test_qa])
            else:
                all_questions.extend([(pre_qa["question"], None) for pre_qa in preliminaries if "answer_hat" not in pre_qa])
                all_questions.extend([(test_qa["question"], None) for test_qa in test_case if "answer_hat" not in test_qa])
        
        if len(all_questions) != 0:
            run_qa(model, all_questions)

        for qa_pair in batch:
            preliminaries = qa_pair["preliminaries"]
            test_case = qa_pair["test"]

            for pre_qa in preliminaries:
                if "answer_hat" in pre_qa:
                    continue
                question = pre_qa["question"]
                answer = pre_qa["answer"]
                if use_context:
                    context = pre_qa["context"]
                else:
                    context = None
                answer_hat = run_qa(model, (question, context))
                pre_qa["answer_hat"] = answer_hat

            for test_qa in test_case:
                if "answer_hat" in test_qa:
                    continue
                question = test_qa["question"]
                answer = test_qa["answer"]
                if use_context:
                    context = test_qa["context"]
                else:
                    context = None
                answer_hat = run_qa(model, (question, context))
                test_qa["answer_hat"] = answer_hat

        if i % 5000 == 0:
            save_dataset(output_path, dataset)
    save_dataset(output_path, dataset)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', "--question", type=str, help="question file")
    parser.add_argument('-o', '--output', type=str, help='output file')
    parser.add_argument('-d', '--device', type=str, default="cpu", help='training device ids')
    parser.add_argument('-m', '--model', type=str, default="unifiedqa", help='qa software')
    parser.add_argument('-nc', '--nocontext', action='store_true', help='use context or not')

    args = parser.parse_args()

    if args.model == "unifiedqa-v2-t5-3b-1251000":
        model = UnifiedQA("allenai/unifiedqa-v2-t5-3b-1251000", device=args.device)
    elif args.model == "unifiedqa-v2-t5-large-1363200":
        model = UnifiedQA("allenai/unifiedqa-v2-t5-large-1363200", device=args.device)
    elif args.model == "unifiedqa-t5-3b":
        model = UnifiedQA("allenai/unifiedqa-t5-3b", device=args.device)
    elif args.model == "unifiedqa-t5-large":
        model = UnifiedQA("allenai/unifiedqa-t5-large", device=args.device)
    elif args.model == "unifiedqa-v2-t5-base-1363200":
        model = UnifiedQA("allenai/unifiedqa-v2-t5-base-1363200", device=args.device)
    elif args.model == "unifiedqa-v2-t5-small-1363200":
        model = UnifiedQA("allenai/unifiedqa-v2-t5-small-1363200", device=args.device)
    else:
        raise Exception("Unknown model name.")
    
    test(args.question, args.output, model, args.device, not args.nocontext)