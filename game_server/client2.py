from game_server.client import Client


server_addr = ('192.168.1.34', 9090)
LOGIN, PASSWORD = 'safin', 'artem'
client = Client(server_addr)

client.set_login('safin')
client.set_password('safin')
client.set_warrior_name('1')
print('Login:', client.login())

client.participate('1')
client.start()
participants_list = client.wait_for_game_start()
print(participants_list, 'participants list')

while True:
    data = input('Data to send: ')
    client.send_data(data)

