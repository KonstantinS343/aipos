from typing import Dict
import logging
import re


class RequestParser:
    def handler(self, data: str) -> Dict[str, str]:
        headers = {}
        print(data)
        request = data.splitlines()
        headers['Request URL'] = re.findall(r'\/[a-zA-Z.\/]*', request[0])[0].strip()
        headers['Request Method'] = re.findall(r'^([A-Z]+)', request[0])[0]
        for i in request:
            if i[:4] == 'Host':
                headers['Host'] = re.findall(r'[a-zA-Z]+:\d+', i)[0]
                break
        logging.info(f'[Request Method] - {headers["Request Method"]}')
        logging.info(f'[Request URL] - {headers["Request URL"]}')
        logging.info(f'[Host] - {headers["Host"]}')
        return headers


class Request:
    def __init__(self, data: bytes) -> None:
        self.__parser = RequestParser()
        self.__headers = self.__parser.handler(data.decode())

    def headers(self) -> Dict[str, str]:
        return self.__headers
