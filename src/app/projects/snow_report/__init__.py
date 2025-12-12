from flask import Blueprint

bp = Blueprint(
    'snow_report',
    __name__,
    url_prefix='/projects/snow_report',
    template_folder='templates',
    static_folder='static'
)

from . import routes