from random import sample, randint
from string import ascii_letters
from time import localtime, asctime, sleep

from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient
CLIENT = OSCClient('localhost', 3002)

def ping_response(*_):
    CLIENT.send_message(b'/ping_response',
        [''.join(sample(ascii_letters, randint(10, 20))).encode('utf8'),])

def send_date():
    CLIENT.send_message(b'/date', [asctime(localtime()).encode('utf8'), ])

if __name__ == '__main__':
    SERVER = OSCThreadServer()
    SERVER.listen('localhost', default=True)
    SERVER.bind(b'/ping', ping_response)
    while True:
        sleep(1)
        send_date()

    SERVER.terminate_server()
    sleep(0.1)
    SERVER.close()



