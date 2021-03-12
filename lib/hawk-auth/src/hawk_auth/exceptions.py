from typing import Optional

from summ_common.exceptions import SummException


class HawkAuthException(SummException):
    DEFAULT_CODE = 1000
    EXCEPTIONS = {
        DEFAULT_CODE: "There was an error that occurred during authentication",
        1001: "Account doesn't exist",
        1002: "Account already exists",
        1003: "Invalid username/password",
        1004: "Credentials invalid or missing",
    }

    def __init__(self, code: int = 1000, message: Optional[str] = None):
        _message = HawkAuthException.EXCEPTIONS.get(code)
        if _message is not None:
            code = code
            _message = _message
        else:
            code = HawkAuthException.DEFAULT_CODE
            _message = HawkAuthException.EXCEPTIONS.get(code)
            if message:
                _message = f"{_message}\n\n{message}"
        super().__init__(code, _message)
