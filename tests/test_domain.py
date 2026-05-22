from tuitor.domain import Answer, Category, Question, QuestionAttempt, Topic, User, Evaluation
from pydantic import ValidationError
import pytest

@pytest.fixture
def category():
    return Category(name="History")

@pytest.fixture
def topic(category):
    return Topic(category_id=category.id, name="WW1")

@pytest.fixture
def question(category, topic):
    return Question(category_id=category.id, topic_id=topic.id, content="Who won the World War I?")

@pytest.fixture
def answer():
    return Answer(content="France")

def test_users_unique_ids():
    user1 = User(name="Jan")
    user2 = User(name="John")
    assert user1.id != user2.id

def test_evaluation_rating_is_within_boundaries():
    with pytest.raises(ValidationError):
        Evaluation(is_correct=True, feedback="Got it SOOOO right", raiting=11)
    with pytest.raises(ValidationError):
        Evaluation(is_correct=False, feedback="Got it SOOOO wrong", raiting=0)

def test_add_new_answers(question):
    question_attempt = QuestionAttempt(question_id=question.id)
    question_attempt.submit_answer(answer_content="Germany")
    question_attempt.submit_answer(answer_content="France")
    assert question_attempt.answers[0].content == "Germany"
    assert question_attempt.answers[1].content == "France"

