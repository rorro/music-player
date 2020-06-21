from flask import Blueprint, render_template, request, jsonify
import os
from urllib.parse import quote
import json
import dbhelper
from functools import wraps

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

    return jsonify(mp3files)

@bp.route("/votes", methods=["GET"])
def get_votes():
    link = request.headers['link']
    token = request.headers['token']

    votes = dbhelper.get_votes(link)
    vote_type = dbhelper.get_vote_type(token, link)

    if votes:
        res_data = {"upvotes": votes[0], "downvotes":votes[1], "vote_type": vote_type}
    else:
        res_data = {"upvotes": 0, "downvotes": 0, "vote_type": None}


    return jsonify(res_data)


@bp.route("/vote", methods=['POST'])
def vote():
    req_data = request.json

    link = req_data['link']
    token = req_data['token']
    vote_type = req_data['type']

    if vote_type == 1:
        dbhelper.upvote(token, link)
    else:
        dbhelper.downvote(token, link)

    votes = dbhelper.get_votes(link);
    if votes:
        res_data = {"upvotes": votes[0], "downvotes": votes[1], "vote_type": vote_type}
    else:
        res_data = {"upvotes": 0, "downvotes": 0, "vote_type": vote_type}

    return jsonify(res_data)

@bp.route("/highlight", methods=["GET"])
def get_highlighted_votes():
    upvotes = request.headers['upvotes']
    downvotes = request.headers['downvotes']

    return jsonify(dbhelper.highlight_votes(upvotes, downvotes))


@bp.route("/filter", methods=['GET'])
def filter_songlist():
    mp3files = []

    filter_type = request.headers['filter_type']
    if filter_type == "upvotes":
        voted_songs = dbhelper.highlight_votes("true", "false")
        songs = voted_songs["upvoted"]
    elif filter_type == "downvotes":
        voted_songs = dbhelper.highlight_votes("false", "true")
        songs = voted_songs["downvoted"]
    else:
        voted_songs = dbhelper.highlight_votes("true", "true")
        songs = voted_songs["upvoted"] + voted_songs["downvoted"]

    for root, dirs, files in os.walk(MUSIC_FOLDER):
        if files:
            for f in files:
                if f.endswith('.mp3'):
                    hit = quote(os.path.join(root, f))
                    if filter_type != "unvoted":
                        if hit in songs:
                            mp3files += [hit]
                    else:
                        if hit not in songs:
                            mp3files += [hit]


    return jsonify(mp3files)
