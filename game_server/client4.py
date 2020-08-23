from game_server.client import Client


server_addr = ('192.168.1.34', 9090)
LOGIN, PASSWORD = 'safin', 'artem'
client = Client(server_addr)

client.set_login('a')
client.set_password('a')
client.set_warrior_name('1')
print('Login:', client.login())

client.participate('1')

participants_list = client.wait_for_game_start()
print(participants_list, 'part. list')
while True:
    data = client.receive_data()
    if data:
        print('Received data:', data)

