import socket
from typing import Dict

from game_server.db.db_funcs import register, login
from game_server.game import Game


class Server:
    def __init__(self):
        self.games: Dict[int, Game] = {}
        self.games_count = 0
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host, self.port = socket.gethostbyname(socket.gethostname()), 9090
        self.sender.bind((self.host, self.port))
        print(f'Started server on {self.host}:{self.port}')

    def process_command(self, command: str, addr):
        if command == 'CREATE':
            self.games_count += 1
            self.games[self.games_count] = Game()
            self.sender.sendto(self.bytes(f'GAME_ID: {self.games_count}'), addr)
            print(f'Created game: {self.games_count}')

        if command.startswith('REGISTER'):
            data = command.split('%')
            user_login, user_password, user_name = data[1:]
            res = register(user_login, user_password, user_name)
            if res:
                self.sender.sendto(bytes('REGISTER: TRUE', encoding='utf-8'), addr)
                print(f'Registered user: {user_login}, {user_password}, {user_name}')
            else:
                print(f'Rejected registration for user: {user_login} with {user_name} '
                      f'because login already exists')
                self.sender.sendto(self.bytes('REGISTER: FALSE'), addr)

        if command.startswith('LOGIN'):
            data = command.split('%')
            user_login, user_password = data[1:]
            res = login(user_login, user_password)
            if res:
                print(f'Login user {user_login}, {user_password}')
                self.sender.sendto(self.bytes('LOGIN:' + '%'.join(str(i) for i in res)), addr)
            else:
                print(f'Rejected login for user {user_login} and {user_password} '
                      f'because something of it is wrong')
                self.sender.sendto(b'LOGIN: FALSE', addr)

        if command.startswith('PARTICIPATE'):
            data = command.split('%')
            user_login, warrior_name, game_id = data[1:]
            self.games[int(game_id)].add_participant(user_login, warrior_name, addr)
            print(f'User ({user_login}, {warrior_name}) participated to game {game_id}')

        if command.startswith('SEND_DATA'):
            game_id, user_login, data = command.split('%')[1:]
            self.games[int(game_id)].send_data(user_login, data)
            print(f'SEND DATA {data} from {user_login} to game {game_id}')

        if command.startswith('RECEIVE_DATA'):
            game_id, user_login = command.split('%')[1:]
            res = 'RECEIVE_DATA:' + self.games[int(game_id)].participants[user_login].get_data()
            self.sender.sendto(self.bytes(res), addr)

        if command.startswith('START'):
            data = command.split('%')
            game_id = data[1]
            answer = 'PARTICIPANTS:' + self.games[int(game_id)].get_participants_list()
            for user in self.games[int(game_id)].participants.values():
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









