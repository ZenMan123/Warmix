from server.flask_app import app
from flask import request, jsonify
import werkzeug


active_games = {}


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/create_game')
def create_game():

    try:
        id = request.args['id']
        creator_id = request.args['creator_id']
    except werkzeug.exceptions.BadRequestKeyError:
        return

    return 'create game'