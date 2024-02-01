from pydantic import BaseModel


class AnswerResponse(BaseModel):
    question: str
    answer: str

    def __str__(self):
        return f"Question: {self.question}\nAnswer: {self.answer}"
