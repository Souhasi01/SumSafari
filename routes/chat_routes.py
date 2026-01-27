# routes/chat_routes.py
import os
from flask import Blueprint, render_template, request, session, jsonify, current_app
from routes.utils import login_required
from extensions import db
from models.chat_message import ChatMessage
from openai import OpenAI

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.route("/chatbot")
@login_required
def chatbot_page():
    return render_template("student/chat.html")

# Load previous chat history
@chat_bp.route("/history", methods=["GET"])
@login_required
def chat_history():
    user_id = session["user_id"]

    messages = ChatMessage.query.filter_by(user_id=user_id) \
        .order_by(ChatMessage.timestamp.asc()).all()

    history = [
        {"sender": m.sender_type, "text": m.message_text}
        for m in messages
    ]

    return jsonify(history)

@chat_bp.route("/send", methods=["POST"])
@login_required
def send_message():
    data = request.get_json() or request.form
    text = data.get("message", "").strip()
    if not text:
        return {"error": "empty message"}, 400

    user_id = session["user_id"]

    # Save user message
    user_msg = ChatMessage(
        user_id=user_id,
        sender_type="user",
        message_text=text,
        timestamp=db.func.now()
    )
    db.session.add(user_msg)
    db.session.commit()

    system_prompt = """
You are TAMBO — a friendly zebra mascot and PSAC-level mathematics tutor.
You ONLY answer PSAC mathematics questions (Grades 4–6 in Mauritius).

RULES:
- Accept ONLY math questions: fractions, decimals, perimeter, area, geometry, measurement,
  patterns, ratios, integers, arithmetic, word problems.
- If outside PSAC math: reply “I can only help with PSAC-level maths.”
- Explain step-by-step in simple child-friendly language.
"""

    try:
        client = OpenAI(api_key=current_app.config["OPENAI_API_KEY"])

        response = client.responses.create(
            model="gpt-5-mini",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            max_output_tokens=1000
        )

        ai_text = response.output_text

    except Exception as e:
        ai_text = "Tambo is thinking… but something went wrong! Please try again later."
        current_app.logger.error(f"OpenAI error: {e}")

    # Save AI reply
    ai_msg = ChatMessage(
        user_id=user_id,
        sender_type="ai",
        message_text=ai_text,
        timestamp=db.func.now()
    )
    db.session.add(ai_msg)
    db.session.commit()

    return jsonify({"reply": ai_text})
