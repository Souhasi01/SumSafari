# routes/auth_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import db
from models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="")

@auth_bp.route("/", methods=["GET"])
def welcome():
    return render_template("welcome.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "student")

        if User.query.filter_by(email=email).first():
            flash("Email already registered. Try logging in.", "danger")
            return redirect(url_for("auth.register"))

        user = User(full_name=full_name, email=email, role=role)
        user.set_password(password)  # model method should hash
        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        selected_role = request.form.get("role")  # ✅ from form

        user = User.query.filter_by(email=email).first()

        # ✅ Check login AND role match
        if user and user.check_password(password) and user.role == selected_role:
            session["user_id"] = user.user_id
            session["user_role"] = user.role
            session["user_name"] = user.full_name

            flash("Logged in successfully.", "success")

            if user.role == "admin":
                return redirect(url_for("admin.admin_home"))

            return redirect(url_for("student.student_home"))

        flash("Invalid credentials or role mismatch.", "danger")
        return redirect(url_for("auth.login"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.welcome"))
