from flask import render_template, redirect, url_for

def register_main_routes(app):

    @app.route("/<path:invalid_path>")
    def catch_all(invalid_path):
        return redirect(url_for('index'))

    @app.route("/")
    def index():
        return render_template("index.html")