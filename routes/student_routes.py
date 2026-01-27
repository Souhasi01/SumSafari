# routes/student_routes.py
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from extensions import db
from routes.utils import login_required
from models.user import User
from models.topic import Topic
from models.quiz import Quiz
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

@student_bp.route("/topics")
@login_required
def topics():
    """
    Displays topic selection page.
    User can:
    - Select ONE topic → topic-based quiz
    - Click 'Test Yourself' → mixed quiz
    """

    topics = Topic.query.order_by(Topic.topic_name).all()
    return render_template("student/topics.html", topics=topics)

@student_bp.route("/progress")
@login_required
def progress():
    user_id = session["user_id"]

    # -------------------------------
    # TOPIC PROGRESS
    # -------------------------------
    summaries = (
        db.session.query(ProgressSummary, Topic.topic_name)
        .join(Topic, ProgressSummary.topic_id == Topic.topic_id)
        .filter(ProgressSummary.user_id == user_id)
        .all()
    )

    progress_data = []

    for summary, topic_name in summaries:
        badge = None
        if summary.accuracy_percentage >= 90:
            badge = "Accuracy Master"
        elif summary.accuracy_percentage >= 75:
            badge = "Proficient"
        elif summary.accuracy_percentage >= 50:
            badge = "Getting There"

        progress_data.append({
            "topic": topic_name,
            "accuracy": round(summary.accuracy_percentage, 2),
            "attempts": summary.attempts_count,
            "badge": badge
        })

    # -------------------------------
    # TEST YOURSELF QUIZZES
    # -------------------------------
    tests = (
        Quiz.query
        .filter(
            Quiz.user_id == user_id,
            Quiz.quiz_type == "full_revision",
            Quiz.completed_at.isnot(None),
            Quiz.score.isnot(None)
        )
        .order_by(Quiz.completed_at.desc())
        .all()
    )

    test_data = []

    for q in tests:
        accuracy = (q.score / q.total_questions) * 100

        badge = None
        if accuracy >= 90:
            badge = "Accuracy Master"
        elif accuracy >= 75:
            badge = "Proficient"
        elif accuracy >= 50:
            badge = "Getting There"

        test_data.append({
            "date": q.completed_at,
            "score": q.score,
            "total": q.total_questions,
            "accuracy": round(accuracy, 2),
            "badge": badge
        })

    # -------------------------------
    # RENDER
    # -------------------------------
    return render_template(
        "student/progress.html",
        progress_data=progress_data,
        test_data=test_data
    )


