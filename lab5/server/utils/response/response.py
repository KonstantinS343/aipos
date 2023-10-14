from typing import Dict
import os

from utils.request.request import Request
from status_code import StatusCodeInt, StatusCodeStr


class ResponseParser:
    def get_parser(self, headers: Dict[str, str | bytes], st_code_int: int, st_code_str: str, path: str):
        files = os.listdir(path)
        response_data = f'HTTP/1.0 {st_code_int} {st_code_str}\r\n'
        response_data += f'Access-Control-Allow-Origin: http://{headers["Host"]}{headers["Request URL"]}\r\n'
        response_data += 'Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n'
        response_data += 'Content-Type: text/html; charset=utf-8\r\n'
        response_data += '\n'
        response_data += """
            <html>
            <body>
            <ul>"""
        for i in files:
            response_data += f'<li><a href="/home/konstantin/bsuir/aipos/lab5/server/storage/{i}">{i}</a></li>\r\n'
        response_data += """
            </ul>
            </body>
            </html>
        """
        return response_data

    def post_parser(self, headers: Dict[str, str | bytes], st_code_int: int, st_code_str: str,
                    uploading_flag: bool = True):
        response_data = f'HTTP/1.0 {st_code_int} {st_code_str}\r\n'
        response_data += f'Access-Control-Allow-Origin: http://{headers["Host"]}{headers["Request URL"]}\r\n'
        response_data += 'Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n'
        response_data += 'Content-Type: text/html; charset=utf-8\r\n'
        response_data += '\n'
        if uploading_flag:
            response_data += """
                <html>
                <body>
                <h1>File uploded!</h1>
                <p>&#128526;</p>
                </body>
                </html>
            """
        else:
            response_data += """
                <html>
                <body>
                <h1>BAD REQUEST</h1>
                </body>
                </html>
            """
        return response_data


class Response:
    def __init__(self, request: Request, storage: str, uploading_flag: bool = True) -> None:
        self.__headers = request.headers()
        self.__parser = ResponseParser()
        self.__uploading_flag = uploading_flag
        self.__storage = storage

    def handle_response(self) -> bytes:
        if self.__headers['Request Method'] == 'GET':
            return self.get()
        elif self.__headers['Request Method'] == 'POST':
            return self.post()

    def get(self) -> bytes:
        response = self.__parser.get_parser(self.__headers,
                                            StatusCodeInt.STATUS_CODE_200.value,
                                            StatusCodeStr.STATUS_CODE_200.value,
                                            path=self.__storage)
        return response.encode()

    def post(self) -> bytes:
        if self.__uploading_flag:
            response = self.__parser.post_parser(self.__headers,
                                                 StatusCodeInt.STATUS_CODE_202.value,
                                                 StatusCodeStr.STATUS_CODE_202.value)
        else:
            response = self.__parser.post_parser(self.__headers,
                                                 StatusCodeInt.STATUS_CODE_400.value,
                                                 StatusCodeStr.STATUS_CODE_400.value,
                                                 False)
        return response.encode()
