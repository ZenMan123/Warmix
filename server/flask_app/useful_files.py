import random


def get_password(length):
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    return ''.join(random.choice(chars) for _ in range(length))
