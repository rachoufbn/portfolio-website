from flask import render_template, jsonify
from .services import SnowReportService
from . import bp

@bp.route("/")
def index():
    return render_template("snow_report/index.html")

@bp.route("/api/get_report")
def get_report():
    try:
        snowReportService = SnowReportService()
        resorts = snowReportService.get_snow_data()
        return jsonify({"success": True, "resorts": resorts})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})