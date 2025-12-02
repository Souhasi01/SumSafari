from extensions import db

class RewardBadge(db.Model):
    __tablename__ = 'reward_badges'

    badge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    badge_name = db.Column(db.String(100))
    icon_path = db.Column(db.String(255))
