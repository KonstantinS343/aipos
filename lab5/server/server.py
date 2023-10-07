import socket
import logging
import configparser
import random

from utils.request.request import Request
from utils.response.response import Response


class HTTPServer:
    BUFFER_SIZE = 1024

    def __init__(self) -> None:
        self.__config = configparser.ConfigParser()
        self.__config.read('server.ini')
        self.__host = 'localhost'  # self.__config['server']['host']
        self.__port = random.randint(1, 10000)

    def run(self):
        server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

        try:
            server.bind((self.__host, self.__port))
            server.listen()
            logging.info(f'Server is running at http://{self.__host}:{self.__port}')
            self.server_loop(server=server)
        except Exception as e:
            print(e)
        finally:
            server.close()

    def server_loop(self, server: socket) -> None:
        try:
            while True:
                connection, addr = server.accept()
                logging.info(f'{addr[0]} connected')

                data = connection.recv(HTTPServer.BUFFER_SIZE)
                request = Request(data)
                response = Response(headers=request.headers())

                connection.sendall(response.handle_response())
                connection.shutdown(socket.SHUT_WR)
                logging.info(f'{addr[0]} disconnected')
        except KeyboardInterrupt:
            logging.info('Shutting down...')
        except Exception as e:
            print('Exception', e)
