import socket
from game_server.create_requests import create_requests





class Client:
    def __init__(self, registered):
        self.login = self.password = self.name = None
        self.registered = registered

        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sender.bind('localhost', 12345)
        self.server_address = ('192.168.1.34', 9090)

    def set_login(self, login):
        self.login = login

    def set_password(self, password):
        self.password = password

    def set_name(self, name):
        self.name = name

    def login(self):
        if not (self.login and self.password):
            return False
        if not self.registered:
            return False
        self.send_command(create_requests('LOGIN', self.login, self.password))
        return self.wait_for_login_confirmation()

    def wait_for_login_confirmation(self):
        while True:
            data = self.sender.recv(150).decode('utf-8')
            if data == 'LOGIN: FALSE':
                return False
            elif data.startswith('LOGIN:'):
                data = data.split('%')
                self.name = data[3]
                return True

    def wait_for_register_confirmation(self):
        while True:
            data = self.sender.recv(150).decode('utf-8')
            if data == 'REGISTER: FALSE':
                return False
            elif data.startswith('REGISTER:'):
                return True

    def send_command(self, request):
        self.sender.sendto(bytes(request, encoding='utf-8'), server_addr)

    def register(self):
        if not (self.name and self.login and self.password):
            return False
        self.send_command(create_requests('REGISTER', self.login, self.password))
        return self.wait_for_register_confirmation()

    @staticmethod
    def create_requests(command, *args):
        arr = [command] + list(args)
        return '%'.join(arr)




server_addr = ('192.168.1.34', 9090)

while True:
    command = input()
    if command == 'login':
        login = input('Login: ')
        password = input('Password: ')
        send_command(create_requests('LOGIN', login, password))
    elif command == 'register':
        login = input('Login: ')
        password = input('Password: ')
        name = input('Name: ')
        send_command(create_requests('REGISTER', login, password, name))
    elif command == 'create':
        send_command('CREATE')
    elif command == 'participate':

LOGIN, PASSWORD = 'safin', 'artem'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 7050))

participate_request = create_requests('PARTICIPATE', LOGIN, '1', str(1))

data_request = create_requests('SEND_DATA', '1', LOGIN, 'my second message')
sock.sendto(bytes(data_request, encoding='utf-8'), server_addr)

while True:
    request = create_requests('RECEIVE_DATA', '1', LOGIN)
    sock.sendto(bytes(request, encoding='utf-8'), server_addr)

    data = sock.recv(150).decode('utf-8')
    print(data)
