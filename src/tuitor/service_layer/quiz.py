from tuitor.domain import Answer, Category, Question, QuestionAttempt, Quiz, Topic, User, Evaluation
from tuitor.identifiers import CategoryId, QuizId, QuestionId, TopicId
def create_quiz(name: str, category_id: CategoryId | None = None, topic_id: TopicId | None = None) -> Quiz:
    if topic_id is not None:
        pass # TODO: When SQLAlchemy session will be implemented add check if topic_id.category_id = category_id
    quiz = Quiz(name=name, category_id=category_id, topic_id=topic_id)
    return quiz

def add_question_to_quiz(quiz_id: QuizId, question_id: QuestionId):
    pass

