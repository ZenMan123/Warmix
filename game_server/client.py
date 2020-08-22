import socket
from game_server.create_requests import create_requests

server_addr = ('localhost', 9090)
LOGIN, PASSWORD = 'e', 'c'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 8080))

sock.sendto(b'CREATE', server_addr)
game_id = sock.recv(150).decode('utf-8')

participate_request = create_requests('PARTICIPATE', LOGIN, '1', str(1))
sock.sendto(bytes(participate_request, encoding='utf-8'), server_addr)

while True:
    request = create_requests('RECEIVE_DATA', '1', LOGIN)
    sock.sendto(bytes(request, encoding='utf-8'), server_addr)
    data = sock.recv(150).decode('utf-8')
    if data:
        print(data)
