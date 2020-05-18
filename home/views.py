from flask import Blueprint, render_template

bp = Blueprint('bp', __name__)

@bp.route("/")
def display_home_view():
    return render_template('index.html')

@bp.route("/<path:path>")
def static_file(path):
    return bp.send_static_file(path)
