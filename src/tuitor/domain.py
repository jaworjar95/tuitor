from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Annotated

from .identifiers import (
    CategoryId, TopicId, UserId, QuizId, QuestionId, QuestionAttemptId, QuizAttemptId,
    new_user_id, new_category_id, new_topic_id, new_quiz_id, new_question_id, new_question_attempt_id, new_quiz_attempt_id,
)

class User(BaseModel):
    id: UserId = Field(default_factory=new_user_id)
    name: str

class Category(BaseModel):
    id: CategoryId = Field(default_factory=new_category_id)
    name: str

class Topic(BaseModel):
    id: TopicId = Field(default_factory=new_topic_id)
    category_id: CategoryId
    name: str

class Question(BaseModel):
    id: QuestionId = Field(default_factory=new_question_id)
    category_id: CategoryId
    topic_id: TopicId | None = None
    content: str

class Quiz(BaseModel):
    id: QuizId = Field(default_factory=new_quiz_id)
    name: str
    category_id: CategoryId | None = None
    topic_id: TopicId | None = None
    question_ids: list[QuestionId] = []
    def add_question(self, question_id: QuestionId) -> None:
        if question_id not in self.question_ids: 
            self.question_ids.append(question_id)
    @model_validator(mode="after")
    def _topic_requires_category(self) -> Quiz:
        if self.topic_id is not None and self.category_id is None:
            raise ValueError("topic_id requires set category_id")
        return self

class Evaluation(BaseModel):
    model_config = ConfigDict(frozen=True)
    is_correct: bool
    rating: Annotated[int, Field(gt=0, lt=11)]
    feedback: str
    hint: str | None = None

class Answer(BaseModel):
    content: str
    evaluation: Evaluation | None = None
    def evaluate(self, is_correct: bool, rating: int, feedback: str, hint: str | None = None) -> Evaluation:
        if self.evaluation is not None:
            raise ValueError(f"Answer was already evaluated: correct: {self.evaluation.is_correct}, rating: {self.evaluation.rating}")
        evaluation = Evaluation(is_correct=is_correct, rating=rating, feedback=feedback, hint=hint)
        self.evaluation = evaluation
        return evaluation


class QuestionAttempt(BaseModel):
    id: QuestionAttemptId = Field(default_factory=new_question_attempt_id)
    question_id: QuestionId
    quiz_attempt_id: QuizAttemptId | None = None
    answers: list[Answer] = []
    solved: bool | None = False
    def submit_answer(self, answer_content: str) -> Answer:
        answer = Answer(content=answer_content)
        self.answers.append(answer)
        return answer
    def is_solved(self) -> bool:
        for answer in reversed(self.answers):
            if answer.evaluation is not None and answer.evaluation.is_correct:
                return True
        return False

class QuizAttempt(BaseModel):
    id: QuizAttemptId = Field(default_factory=new_quiz_attempt_id)
    quiz_id: QuizId
    user_id: UserId

