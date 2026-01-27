import os
from flask import Flask, render_template
from config import Config
from extensions import db, bcrypt  # <- import from extensions

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)

    # Import and register blueprints here
    from routes.auth_routes import auth_bp
    from routes.student_routes import student_bp
    from routes.admin_routes import admin_bp
    from routes.quiz_routes import quiz_bp
    from routes.chat_routes import chat_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(chat_bp)

    # Create all tables
    with app.app_context():
        db.create_all()

    # Keep your home route
    @app.route("/")
    def home():
        return render_template("welcome.html")
    
     # Optional: only create tables if running locally
    if os.environ.get("FLASK_ENV") != "production":
        with app.app_context():
            db.create_all()


    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
