from flask import Blueprint, g
from dotenv import load_dotenv
from .services.repository.database import DatabaseService
from .services.auth import AuthService
import os

load_dotenv()

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
    
db_path = os.getenv('MEETING_NOTES_BOT_DB_PATH')
init_schema_path = os.path.join(os.path.dirname(__file__), 'init.sqlite')

def init_db():
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    db = DatabaseService(db_path)
    with open(init_schema_path) as f:
        db.connection.executescript(f.read())
    db.destroy()

# Make sure the database is initialized at app startup
init_db()

def _register_db_hooks(blueprint):
    """Attach per-request db/auth lifecycle handlers to a blueprint."""

    @blueprint.before_request
    def before_request():
        g.database = DatabaseService(db_path)
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