import socket


class Client:
    def __init__(self, server_addr, login, password):
        self.name = self.warrior_name = None
        self.user_login = login
        self.password = password
        self.authorized = False

        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = server_addr

    def set_name(self, name):
        self.name = name

    def set_warrior_name(self, name):
        self.warrior_name = name

    def login(self):
        self.authorized = self.wait_for_login_confirmation()
        return self.authorized

    def wait_for_login_confirmation(self):
        while True:
            self.send_command(self.create_requests('LOGIN', self.user_login, self.password))
            data = self.sender.recv(150).decode('utf-8')

            if data == 'LOGIN: FALSE':
                return False
            if data.startswith('LOGIN:'):
                data = data.split(':')[1].split('%')
                self.name = data[3]
                return True

    def wait_for_register_confirmation(self):
        while True:
            self.send_command(self.create_requests('REGISTER', self.user_login, self.password, self.name))
            data = self.sender.recv(150).decode('utf-8')

            if data == 'REGISTER: FALSE':
                return False
            if data == 'REGISTER: TRUE':
                return True

    def send_command(self, request):
        self.sender.sendto(bytes(request, encoding='utf-8'), self.server_address)

    def register(self):
        if not (self.name and self.user_login and self.password):
            return False

        self.authorized = self.wait_for_register_confirmation()
        return self.authorized

    def participate(self, game_id):
        if not (self.authorized and self.warrior_name):
            return False

        self.game_id = game_id
        self.send_command(self.create_requests('PARTICIPATE', self.user_login, self.warrior_name, self.game_id))

    def send_data(self, data):
        self.send_command(self.create_requests('SEND_DATA', self.game_id, self.user_login, data))

    def receive_data(self):
        return self.wait_for_data()

    def wait_for_participants_list(self):
        while True:
            data = self.sender.recv(150).decode('utf-8')
            if data.startswith('PARTICIPANTS:'):
                data = data.split(':')[1].split('%')
                return data

    def start(self):
        self.send_command(self.create_requests('START', self.game_id))

    def wait_for_data(self):
        while True:
            self.send_command(self.create_requests('RECEIVE_DATA', self.game_id, self.user_login))
            data = self.sender.recv(150).decode('utf-8')
            if data and data.startswith('RECEIVE_DATA:') and data != 'RECEIVE_DATA:':
                data = data.split(':')[1]
                print('Returned data from wait_for_data:', data)

    def create_game(self):
        if not self.authorized:
            return False

        self.send_command(self.create_requests('CREATE'))
        return self.wait_for_game_id()

    def wait_for_game_id(self):
        while True:
            data = self.sender.recv(150).decode('utf-8')
            if data.startswith('GAME_ID:'):
                return data.split(':')[1]
            else:
                continue

    def wait_for_game_start(self):
        while True:
            data = self.sender.recv(150).decode('utf-8')
            if data.startswith('PARTICIPANTS:'):
                data = data.split(':')[1].split('%')
                return data
            else:
                continue

    @staticmethod
    def create_requests(command, *args):
        arr = [command] + list(args)
        return '%'.join(arr)