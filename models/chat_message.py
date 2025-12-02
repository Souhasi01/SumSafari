from extensions import db

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    sender_type = db.Column(db.Enum('user', 'ai'), nullable=False)
    message_text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
