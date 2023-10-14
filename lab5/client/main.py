import sys
import socket
from typing import Dict
import configparser
import os


def validate(data: Dict[str, str]):
    if data['method'] != 'GET' and data['method'] != 'POST'\
                               and data['method'] != 'OPTIONS':
        raise Exception('The method is wrong')


def client(data: Dict[str, str]):
    config = configparser.ConfigParser()
    config.read('../server/server.ini')
    host = config['server']['host']
    port = int(config['server']['port'])
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    request = ''

    if data['method'] == 'GET':
        request += f'GET / HTTP/1.1\r\nHost: {host}:{port}\r\n'
        client.send(request.encode())
    elif data['method'] == 'POST':
        filename = data['path'].split('/')[-1]
        request += f'POST / HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Length: {os.path.getsize(data["path"])}\r\n\r\n'
        request += f'\r\nContent-Disposition: form-data; name="body"; filename="{filename}"'
        message = (400 - len(request) - 4) * '-'
        message += '\r\n\r\n'
        try:
            file = open(data["path"], "rb")
            client.send((request+message).encode())
            data = file.read(4096)
            while data:
                client.send(data)
                data = file.read(4096)
            file.close()

        except IOError:
            print('You entered an invalid filename!\
                Please enter a valid name')

    while True:
        data = client.recv(4096)
        if len(data) < 1:
            break
        print(data.decode())

    client.close()


if __name__ == '__main__':
    data = dict()
    if len(sys.argv) == 2:
        data['method'] = sys.argv[1]
    elif len(sys.argv) == 3:
        data['method'], data['path'] = sys.argv[1], sys.argv[2]
    else:
        raise Exception('Check your arguments!')
    validate(data)
    client(data)
