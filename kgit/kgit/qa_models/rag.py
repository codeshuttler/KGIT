from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration

def construct_question(question, context):
    question_out = ""
    question_out += question

    if context is not None:
        question_out += " \\n " + context
    return question_out

class RAG(object):
    def __init__(self, model_name, device) -> None:
        '''
        facebook/rag-token-nq
        '''
        self.model_name = model_name
        self.tokenizer = RagTokenizer.from_pretrained(model_name)
        self.retriever = RagRetriever.from_pretrained(model_name, index_name="exact", use_dummy_dataset=True)
        self.model = RagTokenForGeneration.from_pretrained(model_name, retriever=self.retriever)
        self.device = device
        self.model = self.model.to(self.device)

    def run_model(self, input_questions, intput_context):
        input_string = construct_question(input_questions, intput_context).lower()
        input_ids = self.tokenizer.encode(input_string, return_tensors="pt").to(self.device)
        res = self.model.generate(input_ids, max_new_tokens=256)
        return self.tokenizer.batch_decode(res, skip_special_tokens=True)

    def run_model_batch(self, input_questions, intput_context):
        input_string = list([construct_question(q,c).lower() for q,c in zip(input_questions, intput_context)])

        input_dict = self.tokenizer.prepare_seq2seq_batch(input_string, return_tensors="pt")

        input_ids = input_dict["input_ids"].to(self.device)
        generated = self.model.generate(input_ids=input_ids) 
        
        out = self.tokenizer.batch_decode(generated, skip_special_tokens=True)

        return out