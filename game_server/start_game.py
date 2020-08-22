import socket
from game_server.create_requests import create_requests

server_addr = ('localhost', 9090)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 7071))

login_request = create_requests('START', '1')
sock.sendto(bytes(login_request, encoding='utf-8'), server_addr)
