from typing import Optional

from summ_common.exceptions import SummException


class HawkException(SummException):
    DEFAULT_CODE = 0
    EXCEPTIONS = {
        DEFAULT_CODE: "There was an error that occurred",
    }

    def __init__(self, code: int = 0, message: Optional[str] = None):
        _message = HawkException.EXCEPTIONS.get(code)
        if _message is not None and message:
            code = code
            _message = f"{_message}\n\n{message}"
        if not _message:
            code = HawkException.DEFAULT_CODE
            _message = HawkException.EXCEPTIONS[code]
        super().__init__(code, _message)
