from typing import Optional
from transformers import pipeline
import tqdm
import myers
from .utils import chunked

corrector = pipeline(
    'text2text-generation',
    'pszemraj/flan-t5-large-grammar-synthesis',
    device=0
)
CORRECTION_CACHE = {}


def grammar_correct_single(text: Optional[str]):
    if text is None:
        return None
    return corrector(text)

def grammar_correct_batch(text_list: Optional[str], batch_size=32):
    text_out = [None] * len(text_list)
    text_need_correction = []
    for i, text in enumerate(text_list):
        if text is not None:
            text_need_correction.append((text, i))
    batch_out = corrector([b[0] for b in text_need_correction], batch_size=batch_size)
    for i, text_corrected in enumerate(batch_out):
        text_out[text_need_correction[i][1]] = text_corrected["generated_text"]
    return text_out


def grammar_correct(text):
    global CORRECTION_CACHE
    if text is None:
        return None
    
    if isinstance(text, str):
        text_list = [text]
    elif isinstance(text, list):
        text_list = text
    else:
        raise Exception("Unknown Parameter.")
    
    text_out = []
    text_corr = []
    for i, t in enumerate(text_list):
        if t is None:
            text_out.append(None)
        elif t in CORRECTION_CACHE:
            text_out.append(CORRECTION_CACHE[t])
        else:
            text_out.append(None)
            text_corr.append((t, i))
    
    if len(text_corr) != 0:
        text_corr_out = grammar_correct_batch([b[0] for b in text_corr])
        for i, t in enumerate(text_corr_out):
            text_out[text_corr[i][1]] = t
            CORRECTION_CACHE[text_list[text_corr[i][1]]] = t

    if len(text_out) == 1:
        return text_out[0]
    else:
        return text_out


def change_meaning(sentence: str, refined_sentence: str):
    if sentence is None or refined_sentence is None:
        return True
    simple_words = ["a", "the", "an", "for", "in", "at", "on", "off", "of"]
    before_words = sentence.split(" ")
    after_words = refined_sentence.split(" ")
    diff_result = myers.diff(before_words, after_words)

    for i, pair in enumerate(diff_result):
        t, s = pair
        if t.lower() == "r" and s not in simple_words:
            return True
        elif t.lower() == "i" and s not in simple_words:
            return True
    
    return False
            

def check_dataset_grammar(dataset):
    all_questions = []
    all_context = []
    for sample in dataset:
        for qa in sample["preliminaries"]:
            all_questions.append(qa["question"])
            all_context.append(qa["context"])
        for qa in sample["test"]:
            all_questions.append(qa["question"])
            all_context.append(qa["context"])
    
    batch_size = 128
    for batch in tqdm.tqdm(chunked(all_questions, batch_size), total=len(all_questions)//batch_size):
        grammar_correct(batch)
    for batch in tqdm.tqdm(chunked(all_context, batch_size), total=len(all_context)//batch_size):
        grammar_correct(batch)
            
    for sample in tqdm.tqdm(dataset):
        pre_questions = sample["preliminaries"]
        test_questions = sample["test"]
        for qa in pre_questions:
            qa["raw_question"] = qa["question"]
            qa["raw_context"] = qa["context"]
            qa["correction_question"] = grammar_correct(qa["raw_question"])
            qa["correction_context"] = grammar_correct(qa["raw_context"])
            if not change_meaning(qa["raw_question"], qa["correction_question"]):
                qa["question"] = qa["correction_question"]
            else:
                qa["question"] = qa["raw_question"]
            if not change_meaning(qa["raw_context"], qa["correction_context"]):
                qa["context"] = qa["correction_context"]
            else:
                qa["context"] = qa["raw_context"]
        for qa in test_questions:
            qa["raw_question"] = qa["question"]
            qa["raw_context"] = qa["context"]
            qa["correction_question"] = grammar_correct(qa["raw_question"])
            qa["correction_context"] = grammar_correct(qa["raw_context"])
            if not change_meaning(qa["raw_question"], qa["correction_question"]):
                qa["question"] = qa["correction_question"]
            else:
                qa["question"] = qa["raw_question"]
            if not change_meaning(qa["raw_context"], qa["correction_context"]):
                qa["context"] = qa["correction_context"]
            else:
                qa["context"] = qa["raw_context"]