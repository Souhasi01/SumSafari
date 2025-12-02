# routes/quiz_routes.py
import random
from datetime import datetime
from flask import Blueprint, request, session, render_template, redirect, url_for, flash, jsonify, current_app
from extensions import db
from routes.utils import login_required
from models.topic import Topic
from models.question import Question
from models.quiz import Quiz
from models.attempt_answer import AttemptAnswer
from models.progress_summary import ProgressSummary
from models.user_badge import UserBadge
from models.reward_badge import RewardBadge

quiz_bp = Blueprint("quiz", __name__, url_prefix="/quiz")

def select_questions_for_quiz(user_id, selected_topic_ids=None, n_questions=10):
    """
    Simple quiz generation:
    - If selected_topic_ids provided -> sample from those topics
    - Else -> sample from entire question bank
    - Also prioritize previously incorrect questions if any (adaptive)
    """
    # Get previously wrong question IDs for user
    wrong_qs = (
        db.session.query(AttemptAnswer.question_id)
        .join(Quiz, AttemptAnswer.quiz_id == Quiz.quiz_id)
        .filter(Quiz.user_id == user_id, AttemptAnswer.is_correct == False)
        .distinct()
        .all()
    )
    wrong_ids = [r[0] for r in wrong_qs]

    pool_query = Question.query
    if selected_topic_ids:
        pool_query = pool_query.filter(Question.topic_id.in_(selected_topic_ids))

    pool = pool_query.all()
    pool_ids = [q.question_id for q in pool]

    # Start with wrong questions if available
    selected = []
    for qid in wrong_ids:
        if qid in pool_ids and len(selected) < n_questions:
            selected.append(qid)

    # Fill up randomly
    remaining = [pid for pid in pool_ids if pid not in selected]
    random.shuffle(remaining)
    for pid in remaining:
        if len(selected) >= n_questions:
            break
        selected.append(pid)

    return selected

@quiz_bp.route("/start", methods=["GET", "POST"])
@login_required
def start_quiz():
    difficulty = request.args.get("difficulty", "easy")
    data = request.form or request.json or {}

    # ✅ Read from POST form checkboxes
    selected_topics = request.form.getlist("topics")

    # ✅ Also support GET query ?topic_ids=1,2,3
    arg_topics = request.args.get("topic_ids")
    if not selected_topics and arg_topics:
        selected_topics = arg_topics.split(",")

    # ✅ Normalize to int list
    if selected_topics:
        topic_ids = [int(t) for t in selected_topics if t.strip()]
    else:
        topic_ids = []

    # ✅ Determine quiz type
    if len(topic_ids) == 0:
        quiz_type = "full_revision"
    elif len(topic_ids) == 1:
        quiz_type = "topic"
    else:
        quiz_type = "custom"

    n_questions = int(data.get("n_questions", 10))

    # ✅ Create quiz row correctly
    quiz = Quiz(
        user_id=session["user_id"],
        quiz_type=quiz_type,
        selected_topics=",".join(str(t) for t in topic_ids) if topic_ids else "all",
        started_at=datetime.utcnow(),
        total_questions=n_questions
    )
    db.session.add(quiz)
    db.session.flush()

    # ✅ Select questions using correct variable
    selected_qids = select_questions_for_quiz(
        session["user_id"],
        selected_topic_ids=topic_ids,
        n_questions=n_questions
    )

    db.session.commit()

    session["current_quiz"] = {
        "quiz_id": quiz.quiz_id,
        "question_ids": selected_qids,
        "start_time": datetime.utcnow().isoformat()
    }

    questions = Question.query.filter(Question.question_id.in_(selected_qids)).all()
    q_map = {q.question_id: q for q in questions}
    ordered_questions = [q_map[qid] for qid in selected_qids if qid in q_map]

    return render_template(
        "student/quiz.html",
        quiz=quiz,
        questions=ordered_questions,
        quiz_id=quiz.quiz_id,
        difficulty=difficulty
    )


@quiz_bp.route("/check_answer", methods=["POST"])
@login_required
def check_answer():
    """
    AJAX endpoint to check a single answer instantly.
    Expects JSON or form: { question_id: int, answer: str }
    Returns JSON: { is_correct: bool, correct_answer: str, solution_notes: str }
    """
    data = request.get_json(silent=True) or request.form
    qid = int(data.get("question_id"))
    user_ans = (data.get("answer") or "").strip()

    question = Question.query.get(qid)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    correct = (str(user_ans).strip().lower() == str(question.correct_answer).strip().lower())

    return jsonify({
        "is_correct": bool(correct),
        "correct_answer": question.correct_answer,
        "solution_notes": question.solution_notes or ""
    })

@quiz_bp.route("/submit/<int:quiz_id>", methods=["POST"])
@login_required
def submit_quiz(quiz_id):
    """
    Final submit: collects all answers, creates AttemptAnswer rows, updates quiz row,
    updates progress_summary and awards badges if thresholds reached.
    """
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.user_id != session["user_id"]:
        flash("Not authorized to submit this quiz.", "danger")
        return redirect(url_for("student.student_home"))

    # Expect form fields like answer_<question_id>
    answers = {}
    for key, val in request.form.items():
        if key.startswith("answer_"):
            qid = int(key.split("_",1)[1])
            answers[qid] = val.strip()

    correct_count = 0
    total = 0

    # Keep per-topic counts to update progress_summary
    topic_stats = {}  # topic_id -> {correct: int, total: int}

    for qid, user_ans in answers.items():
        question = Question.query.get(qid)
        if not question:
            continue

        is_corr = (str(user_ans).strip().lower() == str(question.correct_answer).strip().lower())

        attempt = AttemptAnswer(
            quiz_id = quiz.quiz_id,
            question_id = qid,
            topic_id = question.topic_id,
            user_answer = user_ans,
            is_correct = bool(is_corr)
        )
        db.session.add(attempt)

        # topic stats
        ts = topic_stats.setdefault(question.topic_id, {"correct":0, "total":0})
        ts["total"] += 1
        if is_corr:
            ts["correct"] += 1
            correct_count += 1

        total += 1

    quiz.completed_at = datetime.utcnow()
    quiz.score = correct_count
    quiz.total_questions = total
    db.session.commit()

    # Update cached progress_summary table per topic
    user_id = quiz.user_id
    for topic_id, stats in topic_stats.items():
        acc = (stats["correct"] / stats["total"]) * 100.0 if stats["total"] > 0 else 0.0
        # find existing summary row
        ps = ProgressSummary.query.filter_by(user_id=user_id, topic_id=topic_id).first()
        if ps:
            # update weighted average or simple recompute: for simplicity we'll replace with latest accuracy and add attempts
            ps.accuracy_percentage = acc
            ps.attempts_count = (ps.attempts_count or 0) + stats["total"]
        else:
            ps = ProgressSummary(
                user_id=user_id,
                topic_id=topic_id,
                accuracy_percentage=acc,
                attempts_count=stats["total"]
            )
            db.session.add(ps)
    db.session.commit()

    # Award badges based on overall accuracy thresholds (you can customize)
    overall_accuracy = (correct_count / total * 100.0) if total else 0.0

    # example thresholds and corresponding badge names (these badges must exist in reward_badges table)
    thresholds = [
        (90, "Accuracy Master"),
        (75, "Proficient"),
        (50, "Getting There")
    ]

    awarded = []
    for thresh, badge_name in thresholds:
        if overall_accuracy >= thresh:
            badge = RewardBadge.query.filter_by(badge_name=badge_name).first()
            if badge:
                # ensure not already awarded
                existing = UserBadge.query.filter_by(user_id=user_id, badge_id=badge.badge_id).first()
                if not existing:
                    ub = UserBadge(user_id=user_id, badge_id=badge.badge_id, awarded_at=datetime.utcnow())
                    db.session.add(ub)
                    awarded.append(badge)
    db.session.commit()

    # calculate time taken using session start_time if available
    start_time_iso = session.get("current_quiz", {}).get("start_time")
    time_taken_seconds = None
    if start_time_iso:
        try:
            start_dt = datetime.fromisoformat(start_time_iso)
            time_taken_seconds = (quiz.completed_at - start_dt).total_seconds()
        except Exception:
            time_taken_seconds = None

    # cleanup session entry
    session.pop("current_quiz", None)

    # Redirect to result page with info
    return redirect(url_for("quiz.quiz_result", quiz_id=quiz.quiz_id))

@quiz_bp.route("/result/<int:quiz_id>")
@login_required
def quiz_result(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.user_id != session["user_id"]:
        flash("Not authorized to view this result.", "danger")
        return redirect(url_for("student.student_home"))

    # fetch attempts
    attempts = AttemptAnswer.query.filter_by(quiz_id=quiz_id).all()

    # compute per-topic summary for display
    per_topic = {}
    for a in attempts:
        t = per_topic.setdefault(a.topic_id, {"correct":0, "total":0})
        t["total"] += 1
        if a.is_correct:
            t["correct"] += 1

    # attach topic names
    topic_objs = Topic.query.filter(Topic.topic_id.in_(per_topic.keys())).all()
    tmap = {t.topic_id: t.topic_name for t in topic_objs}
    per_topic_display = []
    for tid, stats in per_topic.items():
        acc = (stats["correct"] / stats["total"] * 100.0) if stats["total"] else 0.0
        per_topic_display.append({
            "topic_id": tid,
            "topic_name": tmap.get(tid, "Unknown"),
            "accuracy": round(acc,2),
            "correct": stats["correct"],
            "total": stats["total"]
        })

    # badges earned for this user (recent awards included)
    badges = (
        db.session.query(RewardBadge)
        .join(UserBadge, RewardBadge.badge_id == UserBadge.badge_id)
        .filter(UserBadge.user_id == quiz.user_id)
        .all()
    )

    return render_template(
        "student/quiz_result.html",
        quiz=quiz,
        attempts=attempts,
        per_topic=per_topic_display,
        badges=badges
    )
