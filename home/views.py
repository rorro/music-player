from flask import Blueprint, render_template, request, jsonify
import os, glob
from urllib.parse import quote

static_folder = os.path.join(os.pardir, 'static')
MUSIC_FOLDER = "static/music"
bp = Blueprint('bp', __name__, static_folder=static_folder, static_url_path='/static/')

@bp.route("/")
def display_home_view():
    return render_template('index.html')

@bp.route("/<path:path>")
def static_file(path):
    return bp.send_static_file(path)

@bp.route("/songlist", methods=['GET'])
def get_songlist():
    mp3files = []

    for root, dirs, files in os.walk(MUSIC_FOLDER):
        if files:
            mp3files += [quote(os.path.join(root, f)) for f in files if f.endswith('.mp3')]

    print("mp3files:", len(mp3files))

    return jsonify(mp3files)

