import enum


class StatusCodeInt(enum.Enum):
    STATUS_CODE_400 = 400
    STATUS_CODE_202 = 202
    STATUS_CODE_200 = 200
    STATUS_CODE_403 = 403


class StatusCodeStr(enum.Enum):
    STATUS_CODE_400 = 'BAD_REQUEST'
    STATUS_CODE_202 = 'ACCEPTED'
    STATUS_CODE_200 = 'OK'
    STATUS_CODE_403 = 'FORBIDDEN'
