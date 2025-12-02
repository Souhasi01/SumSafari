# routes/admin_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.utils import admin_required
from extensions import db
from models.topic import Topic
from models.question import Question
from models.user import User
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

# Questions CRUD
@admin_bp.route("/questions")
@admin_required
def questions():
    topics = Topic.query.order_by(Topic.topic_name).all()
    return render_template("admin/questions.html", topics=topics)

@admin_bp.route("/questions/add", methods=["POST"])
@admin_required
def add_question():
    topic_id = int(request.form.get("topic_id"))
    question_text = request.form.get("question_text")
    correct_answer = request.form.get("correct_answer")
    difficulty = request.form.get("difficulty", "easy")
    solution_notes = request.form.get("solution_notes", "")

    image_file = request.files.get("question_image")
    filename = None

    # Handle image upload
    if image_file and image_file.filename:
        filename = secure_filename(image_file.filename)
        upload_path = os.path.join("static", "images", "questions", filename)
        image_file.save(upload_path)

    q = Question(
        topic_id=topic_id,
        question_text=question_text,
        correct_answer=correct_answer,
        difficulty=difficulty,
        solution_notes=solution_notes,
        question_image=filename
    )

    db.session.add(q)
    db.session.commit()

    flash("Question added successfully!", "success")
    return redirect(url_for("admin.questions"))


@admin_bp.route("/questions/delete/<int:q_id>", methods=["POST"])
@admin_required
def delete_question(q_id):
    q = Question.query.get_or_404(q_id)
    db.session.delete(q)
    db.session.commit()
    flash("Question removed", "info")
    return redirect(url_for("admin.questions"))

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

    # preload progress + badges to avoid lazy loading problems
    summaries = {
        u.user_id: db.session.query(Topic.topic_name,
                                    ProgressSummary.accuracy_percentage,
                                    ProgressSummary.attempts_count)\
            .join(Topic, Topic.topic_id == ProgressSummary.topic_id)\
            .filter(ProgressSummary.user_id == u.user_id).all()
        for u in students
    }

    badges = {
        u.user_id: db.session.query(RewardBadge.badge_name,
                                    RewardBadge.icon_path)\
            .join(UserBadge, RewardBadge.badge_id == UserBadge.badge_id)\
            .filter(UserBadge.user_id == u.user_id).all()
        for u in students
    }

    return render_template(
        "admin/users.html",
        users=students,
        summaries=summaries,
        badges=badges
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