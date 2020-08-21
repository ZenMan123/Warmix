from server.flask_app import app
from flask import request, jsonify
import werkzeug
from typing import Dict, List
from queue import Queue
from .useful_files import get_password

active_games = [None] * 99999
game_count = 1


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/create_game')
def create_game():
    global game_count, active_games

    try:
        creator_id = request.args['creator_id']
    except werkzeug.exceptions.BadRequestKeyError:
        return jsonify({'status': 404, 'text': 'Не указан creator_id'})

    active_games[game_count] = LastNewsOnGame(creator_id)
    game_count += 1
    return jsonify({'status': 200, 'text': 'OK', 'game_id': game_count - 1})


@app.route('/last_news_on_game')
def get_last_news_on_game():
    global active_games

    try:
        user_id = int(request.args['user_id'])
        game_id = int(request.args['game_id'])
    except werkzeug.exceptions.BadRequestKeyError:
        return jsonify({'status': 404, 'text': 'Не указан user_id или game_id'})
    except ValueError:
        return jsonify({'status': 404, 'text': 'user_id или game_id указан не верно'})

    return jsonify(active_games[game_id].get_last_news(user_id))





# TODO определить эти поля в json
# self.warrior_name = warrior_name
# self.warrior_type = warrior_type
# self.last_side = last_side
# self.modes = modes


class LastNewsOnGame:
    def __init__(self, *warriors_ids):
        self.warriors_ids: List[int] = list(warriors_ids)
        self.last_messages_for_user: Dict[int, Queue[dict]] = {}

    def get_last_news(self, user_id):
        response = {}
        for i in self.warriors_ids:
            if i != user_id:
                if not self.last_messages_for_user[user_id]:
                    response[i] = None
                response[i] = self.last_messages_for_user[user_id].get()
        return response

    def send_last_news(self, user_id: int, news: dict):
        for i in self.warriors_ids:
            if i != user_id:
                self.last_messages_for_user[i].put(news)

    def add_warrior(self, id):
        self.warriors_ids.append(id)
