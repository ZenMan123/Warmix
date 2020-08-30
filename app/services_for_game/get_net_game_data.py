import threading

from app.game.game import Game
from game_server.client import Client


class GetDataThread(threading.Thread):
    def __init__(self, game: Game, client: Client):
        super().__init__()
        self.game = game
        self.client = client

    def run(self):
        while True:
            data = self.client.receive_data()
            mode, last_side, pos = data[1:]
            self.game.warriors[data[0]].update_modes(mode, last_side, pos)
