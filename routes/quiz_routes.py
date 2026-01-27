# routes/quiz_routes.py
from datetime import datetime
from flask import Blueprint, request, session, render_template, redirect, url_for, flash
from extensions import db
from routes.utils import login_required
from models.topic import Topic
from models.quiz import Quiz
from models.progress_summary import ProgressSummary
from models.user_badge import UserBadge
from models.reward_badge import RewardBadge
from quiz_generators.math_questions import generate_quiz

quiz_bp = Blueprint("quiz", __name__, url_prefix="/quiz")


# -------------------------------
# START QUIZ
# -------------------------------
@quiz_bp.route("/start")
@login_required
def start_quiz():

    topic_id = request.args.get("topic_id", type=int)

    # FIXED mapping from DB topic_id → generator code
    TOPIC_CODE_MAP = {
        1: 1,  # Addition, Subtraction, Multiplication & Division
        2: 2,  # Fractions & Decimals
        3: 3,  # Length, Perimeter & Area
        4: 4,  # Patterns, Sequences & Powers
        5: 5,  # Volume & Speed
        6: 6,  # Percentages & Averages
        7: 7,  # Ratio & Proportion
        8: 8,  # Capacity & Mass
        9: 9,  # Money & Time
    }

    topic_code = TOPIC_CODE_MAP.get(topic_id)

    quiz = Quiz(
        user_id=session["user_id"],
        quiz_type="topic" if topic_id else "full_revision",
        selected_topics=str(topic_id) if topic_id else "all",
        started_at=datetime.utcnow(),
        total_questions=5
    )

    db.session.add(quiz)
    db.session.commit()

    questions = generate_quiz(topic_code, 10)

    session["current_quiz"] = {
        "quiz_id": quiz.quiz_id,
        "topic_id": topic_id,
        "questions": questions
    }

    return render_template(
        "student/quiz.html",
        quiz=quiz,
        questions=questions
    )


# -------------------------------
# SUBMIT QUIZ
# -------------------------------
@quiz_bp.route("/submit/<int:quiz_id>", methods=["POST"])
@login_required
def submit_quiz(quiz_id):

    quiz = Quiz.query.get_or_404(quiz_id)

    if quiz.user_id != session["user_id"]:
        flash("Not authorized.", "danger")
        return redirect(url_for("student.student_home"))

    quiz_data = session.get("current_quiz")
    if not quiz_data:
        flash("Quiz session expired.", "warning")
        return redirect(url_for("student.student_home"))

    topic_id = quiz_data.get("topic_id")
    questions = session["current_quiz"]["questions"]
    answers = request.form

    review = []
    score = 0

    for i, q in enumerate(questions, start=1):
        user_ans = answers.get(f"answer_{i}", "").strip()
        is_correct = user_ans == q["answer"]

        if is_correct:
            score += 1

        review.append({
            "question": q["question"],
            "user_answer": user_ans,
            "correct_answer": q["answer"],
            "solution": q.get("solution", ""),
            "is_correct": is_correct
        })

    quiz.score = score
    quiz.completed_at = datetime.utcnow()
    db.session.commit()

    session["quiz_review"] = review

    # -------------------------------
    # UPDATE PROGRESS SUMMARY
    # -------------------------------
    if topic_id:
        accuracy = (score / len(questions)) * 100

        ps = ProgressSummary.query.filter_by(
            user_id=quiz.user_id,
            topic_id=topic_id
        ).first()

        if ps:
            ps.accuracy_percentage = accuracy
            ps.attempts_count = (ps.attempts_count or 0) + 1
        else:
            ps = ProgressSummary(
                user_id=quiz.user_id,
                topic_id=topic_id,
                accuracy_percentage=accuracy,
                attempts_count=1
            )
            db.session.add(ps)

        db.session.commit()

        # -------------------------------
        # ✅ AWARD BADGE (SAVE TO DB)
        # -------------------------------
        badge_name = None

        if accuracy >= 90:
            badge_name = "Accuracy Master"
        elif accuracy >= 75:
            badge_name = "Proficient"
        elif accuracy >= 50:
            badge_name = "Getting There"

        if badge_name:
            badge = RewardBadge.query.filter_by(badge_name=badge_name).first()

            if badge:
                existing = UserBadge.query.filter_by(
                    user_id=quiz.user_id,
                    badge_id=badge.badge_id
                ).first()

                if not existing:
                    db.session.add(
                        UserBadge(
                            user_id=quiz.user_id,
                            badge_id=badge.badge_id,
                            awarded_at=datetime.utcnow()
                        )
                    )
                    db.session.commit()

    return redirect(url_for("quiz.quiz_result", quiz_id=quiz.quiz_id))


# -------------------------------
# QUIZ RESULT
# -------------------------------
@quiz_bp.route("/result/<int:quiz_id>")
@login_required
def quiz_result(quiz_id):

    quiz = Quiz.query.get_or_404(quiz_id)

    if quiz.user_id != session["user_id"]:
        flash("Not authorized.", "danger")
        return redirect(url_for("student.student_home"))

    review = session.get("quiz_review", [])

    topic_performance = []
    test_performance = None
    badge_name = None

    accuracy = (quiz.score / quiz.total_questions) * 100

    # -------------------------------
    # TOPIC QUIZ RESULT
    # -------------------------------
    if quiz.quiz_type == "topic":
        topic_id = int(quiz.selected_topics)
        topic = Topic.query.get(topic_id)

        topic_performance.append({
            "topic_name": topic.topic_name,
            "accuracy": round(accuracy, 2),
            "correct": quiz.score,
            "total": quiz.total_questions
        })

    # -------------------------------
    # TEST YOURSELF RESULT
    # -------------------------------
    else:
        test_performance = {
            "accuracy": round(accuracy, 2),
            "correct": quiz.score,
            "total": quiz.total_questions
        }

    # -------------------------------
    # BADGE LOGIC (SAME FOR BOTH)
    # -------------------------------
    if accuracy >= 90:
        badge_name = "Accuracy Master"
    elif accuracy >= 75:
        badge_name = "Proficient"
    elif accuracy >= 50:
        badge_name = "Getting There"

    return render_template(
        "student/quiz_result.html",
        quiz=quiz,
        review=review,
        topic_performance=topic_performance,
        test_performance=test_performance,
        badge_name=badge_name
    )
