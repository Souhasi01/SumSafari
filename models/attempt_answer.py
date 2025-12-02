from extensions import db

class AttemptAnswer(db.Model):
    __tablename__ = 'attempt_answers'

    attempt_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'), nullable=False)
    user_answer = db.Column(db.String(255))
    is_correct = db.Column(db.Boolean)