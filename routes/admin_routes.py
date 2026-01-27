# routes/admin_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.utils import admin_required
from extensions import db
from models.topic import Topic
from models.user import User
from models.quiz import Quiz
from models.reward_badge import RewardBadge
from models.user_badge import UserBadge
from models.progress_summary import ProgressSummary
from datetime import datetime
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/home")
@admin_required
def admin_home():
    return render_template("admin/home.html")

# Topics CRUD
@admin_bp.route("/topics")
@admin_required
def topics():
    topics = Topic.query.order_by(Topic.topic_name).all()
    return render_template("admin/topics.html", topics=topics)

@admin_bp.route("/topics/add", methods=["POST"])
@admin_required
def add_topic():
    name = request.form.get("topic_name")
    image_file = request.files.get("topic_image")

    if not name:
        flash("Topic name cannot be empty", "danger")
        return redirect(url_for("admin.topics"))

    filename = None

    # Handle image upload
    if image_file and image_file.filename:
        filename = secure_filename(image_file.filename)

        upload_path = os.path.join("static", "images", "topics", filename)
        image_file.save(upload_path)

    # Save topic to DB
    t = Topic(topic_name=name, topic_image=filename)
    db.session.add(t)
    db.session.commit()

    flash("Topic added successfully!", "success")
    return redirect(url_for("admin.topics"))


@admin_bp.route("/topics/delete/<int:topic_id>", methods=["POST"])
@admin_required
def delete_topic(topic_id):
    t = Topic.query.get_or_404(topic_id)
    db.session.delete(t)
    db.session.commit()
    flash("Topic deleted", "info")
    return redirect(url_for("admin.topics"))

# Users view
@admin_bp.route("/users")
@admin_required
def users():
    students = (
        User.query
        .filter_by(role="student")
        .order_by(User.user_id.desc())
        .all()
    )

    user_data = {}

    for u in students:
        # -------------------------------
        # TOPIC PROGRESS
        # -------------------------------
        summaries = (
            db.session.query(
                Topic.topic_name,
                ProgressSummary.accuracy_percentage,
                ProgressSummary.attempts_count
            )
            .join(Topic, Topic.topic_id == ProgressSummary.topic_id)
            .filter(ProgressSummary.user_id == u.user_id)
            .all()
        )

        topic_progress = []
        for topic, accuracy, attempts in summaries:
            badge = None
            if accuracy >= 90:
                badge = "Accuracy Master"
            elif accuracy >= 75:
                badge = "Proficient"
            elif accuracy >= 50:
                badge = "Getting There"

            topic_progress.append({
                "topic": topic,
                "accuracy": round(accuracy, 2),
                "attempts": attempts,
                "badge": badge
            })

        # -------------------------------
        # TEST YOURSELF PERFORMANCE
        # -------------------------------
        tests = (
            Quiz.query
            .filter(
                Quiz.user_id == u.user_id,
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

        user_data[u.user_id] = {
            "topic_progress": topic_progress,
            "test_data": test_data
        }

    return render_template(
        "admin/users.html",
        users=students,
        user_data=user_data
    )


# Badges CRUD
@admin_bp.route("/badges")
@admin_required
def badges():
     b = RewardBadge.query.all()
     return render_template("admin/badges.html", badges=b)

@admin_bp.route("/badges/add", methods=["POST"])
@admin_required
def add_badge():
    name = request.form.get("badge_name")
    icon = request.files.get("icon_path")

    if not name:
        flash("Badge name cannot be empty", "danger")
        return redirect(url_for("admin.badges"))

    filename = None

    # Handle image upload
    if icon and icon.filename:
        filename = secure_filename(icon.filename)

        upload_path = os.path.join("static", "images", "badges", filename)
        icon.save(upload_path)

    # Save badge to DB
    b = RewardBadge(badge_name=name, icon_path=filename)
    db.session.add(b)
    db.session.commit()

    flash("Badge added successfully!", "success")
    return redirect(url_for("admin.badges"))


@admin_bp.route("/badges/delete/<int:badge_id>", methods=["POST"])
@admin_required
def delete_badge(badge_id):
    b = RewardBadge.query.get_or_404(badge_id)
    db.session.delete(b)
    db.session.commit()
    flash("Badge deleted", "info")
    return redirect(url_for("admin.badges"))