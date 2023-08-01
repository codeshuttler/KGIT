import json
import tqdm
import os
import time
import random
import datetime
import neomodel
import neo4j
from kgit.analysis_timer import AnalysisTimer
from kgit.correction import check_dataset_grammar, grammar_correct
from kgit.database import Resource
from kgit.generation.alias_generator import AliasGenerator
from kgit.generation.option_selector import OptionSelector
from kgit.qa import QuestionAnswerPair
from kgit.utils import chunked

random.seed(43)

TEST_RELATIONS = [
    ("Who", "an actor in", "sch__actor"),
    ("What", "the affiliation of", "sch__affiliation"),
    ("Who", "an alumnus of", "sch__alumniOf"),
    ("Who", "the author of", "sch__author"),
    ("Where", "the birthplace of", "sch__birthPlace"),
    ("What", "the brand of", "sch__brand"),
    ("Who", "a character in", "sch__character"),
    ("Who", "a child of", "sch__children"),
    ("What", "the colorist of", "sch__colorist"),
    ("Who", "the competitor of", "sch__competitor"),
    ("Who", "the composer of", "sch__composer"),
    ("Where", "the death place of", "sch__deathPlace"),
    ("Who", "the editor of", "sch__editor"),
    ("What", "the family name of", "sch__familyName"),
    ("What", "the given name of", "sch__givenName"),
    ("What", "the gender of", "sch__gender"),
    ("What", "the home location of", "sch__homeLocation"),
    ("Who", "the organizer of", "sch__organizer"),
    ("Who", "the creator of", "sch__creator"),
    ("What", "the location of", "sch__location"),
    ("Who", "a parent of", "sch__parent"),
    ("Who", "the director of", "sch__director"),
    ("Who", "the founder of", "sch__founder"),
    ("Who", "the producer of", "sch__producer"),
    ("Who", "the provider of", "sch__provider"),
    ("Who", "the publisher of", "sch__publisher"),
    ("Who", "a sponsor of", "sch__sponsor"),
    ("Who", "the translator of", "sch__translator"),
]

def generate_sample(timer, selector, a, b, alter, r1_name, r1_id):
    sample = {
        "preliminaries": [],
        "test": []
    }

    sample["a_name"] = a.label
    sample["a_id"] = a.id
    sample["b_name"] = b.label
    sample["b_id"] = b.id
    sample["alter"] = alter
    sample["r1_id"] = r1_id
    sample["r1_name"] = r1_name

    if r1_id == "sch__gender":
        timer.start_timer("premises_generation")
        sample["preliminaries"].append(QuestionAnswerPair(f"Is {a.label} a {b.label}?", "Yes").to_dict())
        sample["preliminaries"].append(QuestionAnswerPair(f"Is {alter} the alternative name for {a.label}?", "Yes").to_dict())
        timer.end_timer("premises_generation")

        if b.label.lower().strip() == "male":
            another_b = "female"
        else:
            another_b = "male"

        timer.start_timer("question_generation")
        sample["test"].append(
            QuestionAnswerPair(
                f"Is {alter} a {b.label}?",
                "Yes",
                f"{b.label} is {r1_name} {a.label}. {alter} is the alternative name for {a.label}."
            ).to_dict()
        )
        timer.end_timer("question_generation")

        timer.start_timer("ext_question_generation")
        sample["test"].append(
            QuestionAnswerPair(
                f"Is {alter} a {another_b}?",
                "No",
                f"{b.label} is {r1_name} {a.label}. {alter} is the alternative name for {a.label}."
            ).to_dict()
        )
        timer.end_timer("ext_question_generation")
    elif r1_id in ["sch__alumniOf"]:
        
        timer.start_timer("premises_generation")
        sample["preliminaries"].append(QuestionAnswerPair(f"Is {a.label} {r1_name} {b.label}?", "Yes").to_dict())
        sample["preliminaries"].append(QuestionAnswerPair(f"Is {alter} the alternative name for {a}?", "Yes").to_dict())
        timer.end_timer("premises_generation")

        timer.start_timer("question_generation")
        sample["test"].append(
            QuestionAnswerPair(
                f"Is {alter} {r1_name} {b.label}?",
                "Yes",
                f"{a.label} is {r1_name} {b.label}. {alter} is the alternative name for {a.label}."
            ).to_dict()
        )
        timer.end_timer("question_generation")

        timer.start_timer("ext_question_generation")
        options = selector.get_option_list(r1_id, [a.label], limit=5000)
        no_b = random.choice(options)
        sample["test"].append(
            QuestionAnswerPair(
                f"Is {alter} {r1_name} {no_b.label}?",
                "No",
                f"{a.label} is {r1_name} {b.label}. {alter} is the alternative name for {a.label}."
            ).to_dict()
        )
        timer.end_timer("ext_question_generation")
    else:
        
        sample["preliminaries"].append(QuestionAnswerPair(f"Is {b.label} {r1_name} {a.label}?", "Yes").to_dict())
        sample["preliminaries"].append(QuestionAnswerPair(f"Is {alter} the alternative name for {a.label}?", "Yes").to_dict())

        timer.start_timer("question_generation")
        sample["test"].append(
            QuestionAnswerPair(
                f"Is {b.label} {r1_name} {alter}?",
                "Yes",
                f"{b.label} is {r1_name} {a.label}. {alter} is the alternative name for {a.label}."
            ).to_dict()
        )
        timer.end_timer("question_generation")

        timer.start_timer("ext_question_generation")
        options = selector.get_option_list(r1_id, [a], limit=5000)
        no_b = random.choice(options)
        sample["test"].append(
            QuestionAnswerPair(
                f"Is {no_b} {r1_name} {alter}?",
                "No",
                f"{b} is {r1_name} {a}. {alter} is the alternative name for {a}."
            ).to_dict()
        )
        timer.end_timer("ext_question_generation")
    return sample

def main(out_path: str):
    output = []
    timer = AnalysisTimer()
    generator = AliasGenerator()
    selector = OptionSelector()
    for r1 in TEST_RELATIONS:
        r1_qw = r1[0] # question word
        r1_name = r1[1]
        r1_id = r1[2]

        print(r1_id)
        timer.start_timer("knowledge_extraction")
        out = generator.generate(r1_id)
        timer.end_timer("knowledge_extraction")

        for a, alter, b in out:
            if any([n is None for n in (a,alter,b)]):
                continue
            sample = generate_sample(timer, selector, a, b, alter, r1_name, r1_id)
            output.append(sample)
    
    # correct grammar
    timer.start_timer("grammar_correction")
    print("grammar correction")
    check_dataset_grammar(output)
    timer.end_timer("grammar_correction")

    # save
    timer.start_timer("write_to_disk")
    save_dir = os.path.join(out_path, "ir2")
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
    main("./result/")
    end_time = time.time()
    print(f"Time used: {end_time - start_time}s")