from flask import render_template, redirect, url_for, g
from .services.repository.meetings import MeetingsService
from . import bp

@bp.route("/<path:invalid_path>")
def catch_all(invalid_path):
    return redirect(url_for('meeting_notes_bot.index'))

@bp.route("/login")
def login():
    if g.auth_service.is_logged_in():
        return redirect(url_for('meeting_notes_bot.index'))
    return render_template("meeting_notes_bot/login.html")

@bp.route("/")
def index():

    user_id = g.auth_service.get_user_id()

    if user_id is None:
        return redirect(url_for('meeting_notes_bot.login'))

    meetings_service = MeetingsService(g.database, user_id)
    meetings = meetings_service.get()

    user_data = g.auth_service.get_client_side_user_data()

    return render_template("meeting_notes_bot/index.html", user_data=user_data, meetings=meetings)

@bp.route("/meetings/<meeting_id>")
def meeting(meeting_id):

    user_id = g.auth_service.get_user_id()

    if user_id is None:
        return redirect(url_for('meeting_notes_bot.login'))
    
    meetings_service = MeetingsService(g.database, user_id)
    meeting = meetings_service.get(meeting_id)

    # If meeting not found or doesn't belong to user, redirect to index
    if meeting is None:
        return redirect(url_for('meeting_notes_bot.index'))
    
    user_data = g.auth_service.get_client_side_user_data()

    return render_template("meeting_notes_bot/meeting.html", user_data=user_data, meeting=meeting)
