from extensions import db

class Question(db.Model):
    __tablename__ = 'questions'

    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.Enum('easy', 'medium', 'hard'), default="easy")
    solution_notes = db.Column(db.Text)
    question_image = db.Column(db.String(255), nullable=True)
