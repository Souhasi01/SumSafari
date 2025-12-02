from extensions import db

class UserBadge(db.Model):
    __tablename__ = 'user_badges'

    user_badge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    badge_id = db.Column(db.Integer, db.ForeignKey('reward_badges.badge_id'))
    awarded_at = db.Column(db.DateTime)
