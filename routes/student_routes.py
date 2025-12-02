# routes/student_routes.py
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from extensions import db
from routes.utils import login_required
from models.user import User
from models.topic import Topic
from models.quiz import Quiz
from models.attempt_answer import AttemptAnswer
from models.progress_summary import ProgressSummary
from models.user_badge import UserBadge
from models.reward_badge import RewardBadge
from datetime import datetime

student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.route("/home")
@login_required
def student_home():
    return render_template("student/home.html", name=session.get("user_name"))

@student_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = User.query.get(session["user_id"])
    if request.method == "POST":
        user.full_name = request.form.get("full_name", user.full_name)
        # Optionally update password if field present and non-empty
        new_password = request.form.get("password")
        if new_password:
            user.set_password(new_password)
        db.session.commit()
        session["user_name"] = user.full_name
        flash("Profile updated.", "success")
        return redirect(url_for("student.profile"))

    return render_template("student/profile.html", user=user)

@student_bp.route("/topics", methods=["GET", "POST"])
@login_required
def topics():
    topics = Topic.query.order_by(Topic.topic_name).all()

    if request.method == "POST":
        selected = request.form.getlist("topics")
        difficulty = request.form.get("difficulty")

        if not selected:
            flash("Please select at least one topic.", "danger")
            return redirect(url_for("student.topics"))

        # Determine quiz type
        if len(selected) == 1:
            quiz_type = "topic"
        elif len(selected) == len(topics):
            quiz_type = "full_revision"
        else:
            quiz_type = "custom"

        quiz = Quiz(
            user_id=session["user_id"],
            quiz_type=quiz_type,
            selected_topics=",".join(selected),
            started_at=datetime.now()
        )
        db.session.add(quiz)
        db.session.commit()

        # Redirect to quiz page
        return redirect(url_for("quiz.start_quiz", quiz_id=quiz.quiz_id, topic_ids=",".join(selected), difficulty=difficulty))

    return render_template("student/topics.html", topics=topics)

@student_bp.route("/progress")
@login_required
def progress():
    user_id = session["user_id"]

    # Progress summaries
    summaries = (
        db.session.query(ProgressSummary, Topic.topic_name)
        .join(Topic, ProgressSummary.topic_id == Topic.topic_id)
        .filter(ProgressSummary.user_id == user_id)
        .all()
    )

    # Badges earned
    badges = (
        db.session.query(RewardBadge)
        .join(UserBadge, RewardBadge.badge_id == UserBadge.badge_id)
        .filter(UserBadge.user_id == user_id)
        .all()
    )

    return render_template(
        "student/progress.html",
        summaries=summaries,
        badges=badges
    )
