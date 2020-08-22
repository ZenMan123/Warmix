import socket
from game_server.create_requests import create_requests

server_addr = ('localhost', 9090)
LOGIN, PASSWORD = 'safin', 'artem'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 7050))

participate_request = create_requests('PARTICIPATE', LOGIN, '1', str(1))
sock.sendto(bytes(participate_request, encoding='utf-8'), server_addr)

data_request = create_requests('SEND_DATA', '1', LOGIN, 'my second message')
sock.sendto(bytes(data_request, encoding='utf-8'), server_addr)

while True:
    request = create_requests('RECEIVE_DATA', '1', LOGIN)
    sock.sendto(bytes(request, encoding='utf-8'), server_addr)

    data = sock.recv(150).decode('utf-8')
    print(data)
