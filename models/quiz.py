from extensions import db

class Quiz(db.Model):
    __tablename__ = 'quizzes'

    quiz_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    quiz_type = db.Column(db.Enum('topic', 'full_revision', 'custom'))
    selected_topics = db.Column(db.String(255))
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    score = db.Column(db.Integer)
    total_questions = db.Column(db.Integer)

    attempts = db.relationship("AttemptAnswer", backref="quiz", lazy=True)
