from extensions import db

class Topic(db.Model):
    __tablename__ = 'topics'

    topic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic_name = db.Column(db.String(150), nullable=False)
    topic_image = db.Column(db.String(255), nullable=True)
