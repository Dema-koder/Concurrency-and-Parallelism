from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import random

IP_ADDR = '0.0.0.0'
PORT = 12345
BUFF_SIZE = 1024


def generate_random_numbers_string():
    random_numbers = [random.randint(-999999999, 999999999) for _ in range(250000)]
    random_numbers_string = ','.join(map(str, random_numbers))
    return random_numbers_string


class MyThread(Thread):
    def __init__(self, connection, name=None):
        super().__init__(name)
        self.connection = connection

    def run(self):
        nums = generate_random_numbers_string()
        for i in range((len(nums) + BUFF_SIZE - 1) // BUFF_SIZE):
            data = nums[i * BUFF_SIZE: (i + 1) * BUFF_SIZE]
            self.connection.send(data.encode())
        self.connection.close()


try:
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((IP_ADDR, PORT))
        s.listen()
        print(f"Listening on {IP_ADDR}:{PORT}")
        while True:
            conn, addr = s.accept()
            t = MyThread(conn)
            t.start()
            print(f"Sent a file to ({addr})")
except KeyboardInterrupt:
    print("Terminating...")
