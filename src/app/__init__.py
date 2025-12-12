from flask import Flask
from flask_session import Session

def create_app():

    app = Flask(__name__)

    # Session config
    app.config["SESSION_PERMANENT"] = True
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Import project blueprints
    from .projects.meeting_notes_bot import bp as meeting_notes_bot_bp
    from .projects.meeting_notes_bot import api_bp as meeting_notes_bot_api_bp
    from .projects.snow_report import bp as snow_report_bp

    app.register_blueprint(meeting_notes_bot_bp)
    app.register_blueprint(meeting_notes_bot_api_bp)
    app.register_blueprint(snow_report_bp)

    # Import main routes
    from .routes import register_main_routes
    register_main_routes(app)

    return app