import socket


class Client:
    def __init__(self, login, warrior_name):
        self.login = login
        self.warrior_name = warrior_name
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sender.settimeout(5)
        self.server_address = ('192.168.1.34', 9090)
        self.game_id = None

    def create_game(self):
        self.sender.sendto(b'CREATE', self.server_address)
        return self.wait_for_game_id()

    def start_game(self):
        self.sender.sendto(bytes(f'START%{self.game_id}', encoding='utf-8'), self.server_address)
        return self.wait_for_game_start()

    def participate(self, game_id):
        self.game_id = game_id
        self.sender.sendto(bytes(f'PARTICIPATE%{self.login}%{self.warrior_name}%{self.game_id}', encoding='utf-8'),
                           self.server_address)

    def send_data(self, data):
        if data[-2:] != '$;':
            self.sender.sendto(bytes(f'SEND_DATA%{self.login}%{self.game_id}%{data}', encoding='utf-8'),
                               self.server_address)

    def receive_data(self):
        while True:
            try:
                data = self.sender.recv(1024).decode('utf-8')
                if data.startswith('DATA:'):
                    return data.split(':')[1].split('$')
            except socket.timeout:
                continue

    def wait_for_game_start(self):
        while True:
            try:
                data = self.sender.recv(300).decode('utf-8')
                if data.startswith('PARTICIPANTS:'):
                    return data.split('PARTICIPANTS:')[1].split('$')
            except socket.timeout:
                continue


    def wait_for_game_id(self):
        while True:
            try:
                data = self.sender.recv(300).decode('utf-8')
                if data.startswith('GAME_ID:'):
                    return data.split(':')[1]
            except socket.timeout:
                continue
