from typing import Dict
from game_server.user import User


class Game:
    def __init__(self):
        self.participants: Dict[str, User] = {}

    def add_participant(self, user_login, warrior_name, user_addr):
        self.participants[user_login] = User(user_login, warrior_name, user_addr)

    def get_participants_list(self):
        response = []
        for i in self.participants.values():
            response.append(f'{i.user_login}-{i.warrior_name}')
        return '$'.join(response)
