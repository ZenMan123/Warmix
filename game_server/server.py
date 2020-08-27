import socket
from time import time, sleep
from typing import Dict

from game_server.game import Game


class Server:
    address = host, port = socket.gethostbyname(socket.gethostname()), 9090
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self):
        self.games: Dict[int, Game] = {}
        self.games_count = 0
        self.sender.bind((self.host, self.port))
        print(f'Started server on {self.host}:{self.port}')

    def process_command(self, command: str, addr):
        if command == 'CREATE':
            self.games_count += 1
            self.games[self.games_count] = Game()
            self.sender.sendto(self.bytes(f'GAME_ID:{self.games_count}'), addr)
            print(f'Created game: {self.games_count}')

        if command.startswith('PARTICIPATE'):
            data = command.split('%')
            print(data, 'participate')
            user_login, warrior_name, game_id = data[1:]
            self.games[int(game_id)].add_participant(user_login, warrior_name, addr)
            print(f'User ({user_login}, {warrior_name}) participated to game {game_id}')

        if command.startswith('SEND_DATA'):
            print(command)
            user_login, game_id, data = command.split('%')[1:]
            for user in self.games[int(game_id)].participants.values():
                if user.user_login != user_login:
                    self.sender.sendto(bytes(f'DATA:{data}', encoding='utf-8'), user.user_addr)
                    print(f'SEND DATA {data} from {user_login} to {user.user_login}')

        if command.startswith('START'):
            data = command.split('%')
            game_id = data[1]
            answer = 'PARTICIPANTS:' + self.games[int(game_id)].get_participants_list()
            for user in self.games[int(game_id)].participants.values():
                print(user.user_login, answer)
                self.sender.sendto(self.bytes(answer), user.user_addr)
            print(f'Started game {game_id}')

    def bytes(self, message):
        return bytes(str(message), encoding='utf-8')

    def catch_command(self):
        data, addr = self.sender.recvfrom(150)
        try:
            self.process_command(data.decode('utf-8'), addr)
        except Exception as e:
            print(e, 'occurred')


server = Server()
while True:
    server.catch_command()









