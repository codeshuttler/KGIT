from sentence_transformers import SentenceTransformer
from scipy import spatial


def calculate_cosine_distance(a, b):
    cosine_distance = float(spatial.distance.cosine(a, b))
    return cosine_distance

embedding_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', device="cuda")
yes_embedding = embedding_model.encode('yes')
no_embedding = embedding_model.encode('no')

def check_answer_yesno(ground_truth: str, qa_answer: str):
    ground_truth_clean = ground_truth.strip().lower()
    if ground_truth_clean == "yes":
        return "yes" in qa_answer.strip().lower()
    elif ground_truth_clean == "no":
        return "no" in qa_answer.strip().lower()
    else:
        sentence_embeddings = embedding_model.encode(qa_answer.strip().lower())
        yes_dist = calculate_cosine_distance(sentence_embeddings, yes_embedding)
        no_dist = calculate_cosine_distance(sentence_embeddings, yes_embedding)
        threshold = 0.5
        if ground_truth_clean == "yes":
            return yes_dist < threshold
        elif ground_truth_clean == "no":
            return no_dist < threshold

def check_answer_normal(ground_truth: str, qa_answer: str):
    if ground_truth.strip().lower() == "yes":
        return "yes" in qa_answer.strip().lower()
    elif ground_truth.strip().lower() == "no":
        return "no" in qa_answer.strip().lower()
    else:
        return ground_truth.strip().lower() == qa_answer.strip().lower()

def check_answer(ground_truth: str, qa_answer: str):
    '''
    True: 答案一致
    False: 答案不一致
    '''
    ground_truth_clean = ground_truth.strip().lower()
    if "yes" in ground_truth_clean or "no" in ground_truth_clean:
        return check_answer_yesno(ground_truth, qa_answer)
    else:
        return check_answer_normal(ground_truth, qa_answer)