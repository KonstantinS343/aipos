from typing import Dict
import logging
import re


class RequestParser:
    def __init__(self, data: bytes) -> None:
        try:
            headers, file_info, body = data.split(b'\r\n\r\n')
        except Exception:
            error_split = True
            headers, file_info = data.split(b'\r\n\r\n')
        else:
            error_split = False
        request = (headers+file_info).decode().splitlines()
        self.__request = {'head': request[0]}
        for i in request[1:]:
            try:
                key, value = i.split(': ')
            except Exception:
                if key == 'Content-Type':
                    break
                continue
            self.__request[key] = value

        if not error_split:
            self.__request['body'] = body

    def handler(self) -> Dict[str, str]:
        self.__request['Request URL'] = re.findall(r'\/[a-zA-Z.\/]*', self.__request['head'])[0].strip()
        self.__request['Request Method'] = re.findall(r'^([A-Z]+)', self.__request['head'])[0]
        logging.info(f'[Request Method] - { self.__request["Request Method"]}')
        logging.info(f'[Request URL] - { self.__request["Request URL"]}')
        logging.info(f'[Host] - { self.__request["Host"]}')
        logging.info(f'[Content-Type] - { self.__request["Content-Type"]}')
        return self.__request


class Request:
    def __init__(self, data: bytes) -> None:
        self.__parser = RequestParser(data=data)
        self.__headers = self.__parser.handler()

    def headers(self) -> Dict[str, str]:
        return self.__headers
