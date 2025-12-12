from flask import Blueprint, g
from dotenv import load_dotenv
from .services.repository.database import DatabaseService
from .services.auth import AuthService
import os

bp = Blueprint(
    'meeting_notes_bot',
    __name__,
    url_prefix='/projects/meeting_notes_bot',
    template_folder='templates',
    static_folder='static'
)

api_bp = Blueprint(
    'meeting_notes_bot_api',
    __name__,
    url_prefix='/projects/meeting_notes_bot/api',
    template_folder=None,
    static_folder=None
)

load_dotenv()

DatabaseService.initialize_pool(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    user='meeting_notes_bot',
    password=os.getenv('MEETING_NOTES_BOT_DB_PASS'),
    database='meeting_notes_bot'
)

def _register_db_hooks(blueprint):
    """Attach per-request db/auth lifecycle handlers to a blueprint."""

    @blueprint.before_request
    def before_request():
        g.database = DatabaseService()
        g.auth_service = AuthService(g.database)

    @blueprint.teardown_request
    def teardown(exception):
        database = getattr(g, 'database', None)
        if database is not None:
            database.destroy()

_register_db_hooks(bp)
_register_db_hooks(api_bp)

from . import routes
from . import api_routes