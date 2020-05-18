from flask import Blueprint, render_template
import os

static_folder = os.path.join(os.pardir, 'static')
bp = Blueprint('bp', __name__, static_folder=static_folder, static_url_path='/static/')

@bp.route("/")
def display_home_view():
    return render_template('index.html')

@bp.route("/<path:path>")
def static_file(path):
    return bp.send_static_file(path)
