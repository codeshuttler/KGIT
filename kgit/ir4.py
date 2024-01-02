# 反向关系
import argparse
import json
import os
import time
import tqdm
import random
from kgit.database import Resource
from kgit.generation.single_generator import SingleGenerator
from kgit.qa import QuestionAnswerPair
from kgit.utils import chunked
from kgit.generation.option_selector import OptionSelector
from kgit.analysis_timer import AnalysisTimer

random.seed(43)

TEST_RELATIONS = [
    ("What", "a part of", "sch__hasPart"),
    ("Who", "a parent of", "sch__parent"),
    ("Who", "a child of", "sch__children"),

    ("Who", "the author of", "sch__author"),
    ("Who", "the editor of", "sch__editor"),
    ("Who", "the creator of", "sch__creator"),
    ("Who", "the organizer of", "sch__organizer"),
    ("Who", "the director of", "sch__director"),
    ("Who", "the founder of", "sch__founder"),
    ("Who", "the producer of", "sch__producer"),
    ("Who", "the provider of", "sch__provider"),
    ("Who", "the publisher of", "sch__publisher"),
    ("Who", "a sponsor of", "sch__sponsor"),
    ("Who", "the translator of", "sch__translator"),
    ("What", "the colorist of", "sch__colorist"),
    ("Who", "the competitor of", "sch__competitor"),
    ("Who", "the composer of", "sch__composer"),
]

def generate_sample(timer, selector, a, b, r1_name, r1_id):
    sample = {
        "preliminaries": [],
        "test": []
    }

    sample["a_name"] = a.label
    sample["a_id"] = a.id
    sample["b_name"] = b.label
    sample["b_id"] = b.id
    sample["r1_id"] = r1_id
    sample["r1_name"] = r1_name

    timer.start_timer("premises_generation")
    sample["preliminaries"].append(QuestionAnswerPair(f"Is {b.label} {r1_name} {a.label}?", "Yes").to_dict())
    timer.end_timer("premises_generation")

    timer.start_timer("question_generation")
    sample["test"].append(QuestionAnswerPair(
        f"Is {a.label} {r1_name} {b.label}?",
        "No",
        f"{b.label} is {r1_name} {a.label}."
        ).to_dict())
    timer.end_timer("question_generation")

    timer.start_timer("ext_question_generation")
    options = selector.get_option_list_target_not(r1_id, [b.label], limit=5000)
    no_a = random.choice(options)
    sample["test"].append(QuestionAnswerPair(
        f"Is {b.label} {r1_name} {no_a.label}?",
        "No",
        f"{b.label} is {r1_name} {a.label}."
        ).to_dict())
    timer.end_timer("ext_question_generation")
    
    return sample

def main():
    parser = argparse.ArgumentParser(description='Command Line Arguments')
    parser.add_argument('--check-grammar', action='store_true', help='Check grammar')
    parser.add_argument('--out-path', type=str, default="./result/", help='Output path')

    args = parser.parse_args()

    output = []
    timer = AnalysisTimer()
    generator = SingleGenerator()
    selector = OptionSelector()
    for r1 in TEST_RELATIONS:
        r1_qw = r1[0] # question word
        r1_name = r1[1]
        r1_id = r1[2]

        print(r1_id)
        timer.start_timer("knowledge_extraction")
        out = generator.generate(r1_id)
        timer.end_timer("knowledge_extraction")

        for a, b in out:
            if any([n is None for n in (a.label, b.label)]):
                continue
            sample = generate_sample(timer, selector, a, b, r1_name, r1_id)
            output.append(sample)

    # correct grammar
    timer.start_timer("grammar_correction")
    if args.check_grammar:
        from kgit.correction import check_dataset_grammar, grammar_correct
        print("grammar correction")
        check_dataset_grammar(output)
    timer.end_timer("grammar_correction")

    # save
    timer.start_timer("write_to_disk")
    save_dir = os.path.join(args.out_path, "kr4")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, "questions.txt"), "w", encoding="utf-8") as f:
        for sample in output:
            f.write(json.dumps(sample) + '\n')
    timer.end_timer("write_to_disk")

    # print timer
    print(timer.get_summary())

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Time used: {end_time - start_time}s")