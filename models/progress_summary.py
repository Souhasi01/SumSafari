from extensions import db

class ProgressSummary(db.Model):
    __tablename__ = 'progress_summary'

    summary_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'))
    accuracy_percentage = db.Column(db.Numeric(5, 2))
    attempts_count = db.Column(db.Integer)
