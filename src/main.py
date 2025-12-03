from flask import Flask, render_template, jsonify
#from projects.snow_report.service import get_test_data
from projects.snow_report.snow_report import get_snow_data

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/snow_report")
def snow_report():
    return render_template("snow_report.html")

@app.route("/api/snow_report")
def snow_report_api():
    try:
        resorts = get_snow_data()
        return jsonify({"success": True, "resorts": resorts})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})