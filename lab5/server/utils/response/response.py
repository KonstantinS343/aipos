from typing import Dict

from status_code import StatusCodeInt, StatusCodeStr


class ResponseParser:
    def parse_response(self, headers: Dict[str, str]):
        response_data = f'HTTP/1.0 {StatusCodeInt.STATUS_CODE_200.value} {StatusCodeStr.STATUS_CODE_200.value}\n'
        response_data += f'Access-Control-Allow-Origin: http://{headers["Host"]}{headers["Request URL"]}'
        response_data += 'Access-Control-Allow-Methods: GET, POST, OPTIONS'
        response_data += 'Content-Type: text/html; charset=utf-8\n'
        response_data += '\n'
        response_data += """
            <html>
            <body>
            <h1>Hello World</h1> this is my server!
            </body>
            </html>
        """
        return response_data


class Response:
    def __init__(self, headers: Dict[str, str]) -> None:
        self.__headers = headers
        self.__parser = ResponseParser()

    def handle_response(self) -> bytes:
        if self.__headers['Request Method'] == 'GET':
            return self.get()
        elif self.__headers['Request Method'] == 'POST':
            return self.post()

    def get(self) -> bytes:
        response = self.__parser.parse_response()
        return response.encode()

    def post(self) -> bytes:
        pass
