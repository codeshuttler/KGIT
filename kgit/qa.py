

from typing import Dict, Optional


class QuestionAnswerPair(object):
    def __init__(self, question: str, answer: str, context: Optional[str]=None) -> None:
        self.question = question
        self.answer = answer
        self.context = context

    def __str__(self) -> str:
        return f"({self.question}, {self.answer}, {self.context})"
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "question": self.question,
            "answer": self.answer,
            "context": self.context
        }