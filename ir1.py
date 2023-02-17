import json
import time
import random
import tqdm
import os
import argparse
import datetime
from kgit.analysis_timer import AnalysisTimer
from kgit.database import Resource
from kgit.generation.composition_generator import CompositionGenerator
from kgit.generation.option_selector import OptionSelector
from kgit.qa import QuestionAnswerPair
from kgit.correction import check_dataset_grammar, grammar_correct
from kgit.utils import chunked

random.seed(43)

SELECTED_RELATIONS = [
    ("Who", "the author of", "sch__author"),
    ("Who", "the editor of", "sch__editor"),
    ("Who", "the creator of", "sch__creator"),
    ("Who", "the organizer of", "sch__organizer"),
    ("Who", "the director of", "sch__director"),
    ("Who", "the founder of", "sch__founder"),
    ("Who", "the producer of", "sch__producer"),
    ("Who", "the provider of", "sch__provider"),
    ("Who", "the publisher of", "sch__publisher"),
    ("Who", "the translator of", "sch__translator"),
    ("What", "the colorist of", "sch__colorist"),
    ("Who", "the composer of", "sch__composer"),
]
TEST_RELATIONS = [
    ("What", "the affiliation of", "sch__affiliation"),
    ("What", "an alumnus of", "sch__alumniOf"),
    ("Where", "the birthplace of", "sch__birthPlace"),
    ("Who", "a child of", "sch__children"),
    ("Where", "the death place of", "sch__deathPlace"),
    ("What", "the family name of", "sch__familyName"),
    ("What", "the given name of", "sch__givenName"),
    ("What", "the gender of", "sch__gender"),
    ("What", "the home location of", "sch__homeLocation"),
    ("What", "the location of", "sch__location"),
    ("Who", "a parent of", "sch__parent"),
]

def generate_sample(timer, selector, a, b, c, r1_name, r1_id, r2_name, r2_id):
    sample = {
        "preliminaries": [],
        "test": []
    }

    sample["a_name"] = a.label
    sample["a_id"] = a.id
    sample["b_name"] = b.label
    sample["b_id"] = b.id
    sample["c_name"] = c.label
    sample["c_id"] = c.id
    sample["r1_id"] = r1_id
    sample["r1_name"] = r1_name
    sample["r2_id"] = r2_id
    sample["r2_name"] = r2_name

    if r2_id == "sch__gender":
        timer.start_timer("premises_generation")
        sample["preliminaries"].append(QuestionAnswerPair(f"Is {b.label} {r1_name} {a.label}?", "Yes").to_dict())
        sample["preliminaries"].append(QuestionAnswerPair(f"Is {b.label} a {c.label}?", "Yes").to_dict())
        timer.end_timer("premises_generation")

        if c.label.lower().strip() == "male":
            another_c = "female"
        else:
            another_c = "male"
        
        timer.start_timer("question_generation")
        sample["test"].append(
            QuestionAnswerPair(
                f"Is {r1_name} {a.label} a {c.label}?",
                "Yes",
                f"{b.label} is {r1_name} {a.label}. {c.label} is {r2_name} {b.label}."
            ).to_dict()
        )
        timer.end_timer("question_generation")

        sample["test"].append(
            QuestionAnswerPair(
                f"Is {r1_name} {a.label} a {another_c}?",
                "No",
                f"{b.label} is {r1_name} {a.label}. {c.label} is {r2_name} {b.label}."
            ).to_dict()
        )
    elif r2_id in ["sch__alumniOf"]:
        timer.start_timer("premises_generation")
        sample["preliminaries"].append(QuestionAnswerPair(f"Is {b.label} {r1_name} {a.label}?", "Yes").to_dict())
        sample["preliminaries"].append(QuestionAnswerPair(f"Is {b.label} {r2_name} {c.label}?", "Yes").to_dict())
        timer.end_timer("premises_generation")

        timer.start_timer("question_generation")
        sample["test"].append(
            QuestionAnswerPair(
                f"Is {r1_name} {a.label} {r2_name} {c.label}?",
                "Yes",
                f"{b.label} is {r1_name} {a.label}. {b.label} is {r2_name} {c.label}."
            ).to_dict()
        )
        timer.end_timer("question_generation")

        timer.start_timer("ext_question_generation")
        options = selector.get_option_list(r2_id, [b.label], limit=5000)
        no_c = random.choice(options)
        sample["test"].append(
            QuestionAnswerPair(
                f"Is {r1_name} {a.label} {r2_name} {no_c.label}?",
                "No",
                f"{b.label} is {r1_name} {a.label}. {b.label} is {r2_name} {c.label}."
            ).to_dict()
        )
        timer.end_timer("ext_question_generation")
    else:
        timer.start_timer("premises_generation")
        sample["preliminaries"].append(QuestionAnswerPair(f"Is {b.label} {r1_name} {a.label}?", "Yes").to_dict())
        sample["preliminaries"].append(QuestionAnswerPair(f"Is {c.label} {r2_name} {b.label}?", "Yes").to_dict())
        timer.end_timer("premises_generation")

        timer.start_timer("question_generation")
        sample["test"].append(
            QuestionAnswerPair(
                f"Is {c.label} {r2_name} {r1_name} {a.label}?",
                "Yes",
                f"{b.label} is {r1_name} {a.label}. {c.label} is {r2_name} {b.label}."
            ).to_dict()
        )
        timer.end_timer("question_generation")

        timer.start_timer("ext_question_generation")
        options = selector.get_option_list(r2_id, [b.label], limit=5000)
        no_c = random.choice(options)
        sample["test"].append(
            QuestionAnswerPair(
                f"Is {no_c.label} {r2_name} {r1_name} {a.label}?",
                "No",
                f"{b.label} is {r1_name} {a.label}. {c.label} is {r2_name} {b.label}."
            ).to_dict()
        )
        timer.end_timer("ext_question_generation")
    return sample

def main(out_path: str):
    
    output = []
    timer = AnalysisTimer()
    generator = CompositionGenerator()
    selector = OptionSelector()
    for r1 in SELECTED_RELATIONS:
        r1_qw = r1[0] # question word
        r1_name = r1[1]
        r1_id = r1[2]
        for r2 in TEST_RELATIONS:
            r2_qw = r2[0] # question word
            r2_name = r2[1]
            r2_id = r2[2]

            print(r1_id, r2_id)
            timer.start_timer("knowledge_extraction")
            out = generator.generate(r1_id, r2_id)
            timer.end_timer("knowledge_extraction")

            for a, b, c in out:
                if any([n is None for n in (a.label, b.label, c.label)]):
                    continue
                sample = generate_sample(timer, selector, a, b, c, r1_name, r1_id, r2_name, r2_id)
                output.append(sample)
    
    # correct grammar
    timer.start_timer("grammar_correction")
    print("grammar correction")
    check_dataset_grammar(output)
    timer.end_timer("grammar_correction")

    # save
    timer.start_timer("write_to_disk")
    save_dir = os.path.join(out_path, "ir1")
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