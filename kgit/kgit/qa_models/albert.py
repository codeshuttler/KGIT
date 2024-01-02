import torch
from transformers import AlbertTokenizer, AlbertForQuestionAnswering

class Albert(object):
    def __init__(self, device) -> None:
        self.model_name = "./models/albert-xxlarge-v2" # "allenai/unifiedqa-v2-t5-11b-1363200" # "allenai/unifiedqa-t5-large" # you can specify the model size here
        self.tokenizer = AlbertTokenizer.from_pretrained(self.model_name)
        self.model = AlbertForQuestionAnswering.from_pretrained(self.model_name)
        self.device = device
        self.model = self.model.to(self.device)

    def run_model(self, input_questions, intput_context, **generator_args):
        input_ids = self.tokenizer.encode(input_questions, intput_context, return_tensors="pt").to(self.device)
        res = self.model.generate(input_ids, **generator_args)
        return self.tokenizer.batch_decode(res, skip_special_tokens=True)

    def run_model_batch(self, input_questions, intput_context, **generator_args):
        intput_context_replaced = []
        for context in intput_context:
            if context is None:
                intput_context_replaced.append("")
            else:
                intput_context_replaced.append(context)
        # print("tokenizer start")
        input_ids = self.tokenizer(input_questions, intput_context_replaced, return_tensors="pt", padding=True).to(self.device)
        # print("tokenizer end")

        # print("generation start")
        with torch.no_grad():
            res = self.model(**input_ids, **generator_args)
        # print("generation end")

        # print("decode start")
        out = self.tokenizer.batch_decode(res.input_ids, skip_special_tokens=True)
        # print("decode end")
        return out