from transformers import T5Tokenizer, T5ForConditionalGeneration

def construct_question(question, context):
    question_out = ""
    question_out += question

    if context is not None:
        question_out += " \\n " + context
    return question_out

class BertSerini(object):
    def __init__(self, model_name, device) -> None:
        self.model_name = model_name # "allenai/unifiedqa-v2-t5-11b-1363200" # "allenai/unifiedqa-t5-large" # you can specify the model size here
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
        self.device = device
        self.model = self.model.to(self.device)

    def run_model(self, input_questions, intput_context):
        input_string = construct_question(input_questions, intput_context).lower()
        input_ids = self.tokenizer.encode(input_string, return_tensors="pt").to(self.device)
        res = self.model.generate(input_ids, max_new_tokens=256)
        return self.tokenizer.batch_decode(res, skip_special_tokens=True)

    def run_model_batch(self, input_questions, intput_context):
        input_string = list([construct_question(q,c).lower() for q,c in zip(input_questions, intput_context)])
        # print("tokenizer start")
        input_ids = self.tokenizer(input_string, return_tensors="pt", padding=True).to(self.device)
        # print("tokenizer end")

        # print("generation start")
        res = self.model.generate(**input_ids, max_new_tokens=256)
        res = res.to("cpu")
        # print("generation end")

        # print("decode start")
        out = self.tokenizer.batch_decode(res, skip_special_tokens=True)
        # print("decode end")
        return out