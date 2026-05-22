from pydantic import BaseModel, ConfigDict, Field
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
    question_ids: list[QuestionId] = []
    def add_question(self, question_id: QuestionId) -> None:
        if question_id not in self.question_ids: 
            self.question_ids.append(question_id)

class Evaluation(BaseModel):
    model_config = ConfigDict(frozen=True)
    rating: Annotated[int, Field(gt=0, lt=11)]
    feedback: str
    hint: str | None = None

class Answer(BaseModel):
    content: str
    evaluation: Evaluation | None = None

class QuestionAttempt(BaseModel):
    id: QuestionAttemptId = Field(default_factory=new_question_attempt_id)
    question_id: QuestionId
    quiz_attempt_id: QuizAttemptId | None = None
    answers: list[Answer] = []
    def submit_answer(self, answer_content) -> Answer:
        answer = Answer(content=answer_content)
        self.answers.append(answer)
        return answer

class QuizAttempt(BaseModel):
    id: QuizAttemptId = Field(default_factory=new_quiz_attempt_id)
    quiz_id: QuizId
    user_id: UserId

