import socket
import logging
import configparser
import re

from utils.request.request import Request
from utils.response.response import Response
from utils.file_share import FileHandler


class HTTPServer:
    BUFFER_SIZE = 4096

    def __init__(self) -> None:
        self.__config = configparser.ConfigParser()
        self.__config.read('server.ini')
        self.__host = self.__config['server']['host']
        self.__port = int(self.__config['server']['port'])
        self.__storage = self.__config['server']['storage_path']
        self.__file = FileHandler(self.__storage)

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
            logging.info(e)
        finally:
            server.close()

    def server_loop(self, server: socket) -> None:
        try:
            while True:
                connection, addr = server.accept()

                logging.info(f'{addr[0]} connected')

                data: bytes = connection.recv(400)
                str_data = data.decode()
                try:
                    request_length = re.findall(r'Content-Length: \d+', str_data)[0]
                except Exception:
                    pass
                else:
                    _, request_length = request_length.split('Content-Length: ')
                    content_length, request_length = len(data), int(request_length)

                    while content_length < request_length:
                        read_bytes = connection.recv(HTTPServer.BUFFER_SIZE)
                        data += read_bytes
                        content_length += len(read_bytes)
                request = Request(data)
                uploading = self.__file.upload(request.headers())
                response = Response(request=request, storage=self.__storage, uploading_flag=uploading)

                connection.sendall(response.handle_response())
                connection.shutdown(socket.SHUT_WR)
                logging.info(f'{addr[0]} disconnected')
        except KeyboardInterrupt:
            logging.info('Shutting down...')
        except Exception as e:
            logging.info(e)
