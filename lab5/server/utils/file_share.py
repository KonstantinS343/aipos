from typing import Dict


class FileHandler:
    def __init__(self) -> None:
        self.__path = '/home/konstantin/bsuir/aipos/lab5/server/storage/'

    def upload(self, headers: Dict[str, str | bytes]) -> bool:
        try:
            data_bytes = headers['body']
            filename_begin = headers['Content-Disposition'].find('filename="') + len('filename="')
            filename_end = headers['Content-Disposition'].find('"', filename_begin)
            filename = headers['Content-Disposition'][filename_begin:filename_end]
            with open(self.__path + filename, 'wb') as file:
                file.write(data_bytes)
        except Exception:
            return False
        else:
            return True
