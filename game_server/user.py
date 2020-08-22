from typing import List


class User:
    def __init__(self, user_login, warrior_name, user_addr):
        self.user_login = user_login
        self.warrior_name = warrior_name
        self.user_addr = user_addr
        self.mailbox: List[str] = []

    def add_data(self, data):
        self.mailbox.append(data)

    def get_data(self):
        temp = self.mailbox.copy()
        self.mailbox.clear()
        return '%'.join(temp)