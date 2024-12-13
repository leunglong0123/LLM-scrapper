from typing import Any, Dict
from model.Error.ErrorModel import ErrorModel, ErrorCode


class ResponseModel(ErrorModel):
    def __init__(self, code: int, data: Dict[str, Any]):
        self.code = code
        self.data = data

    @property
    def data(self) -> dict:
        return self._data

    @data.setter
    def data(self, value: dict):
        self._data = value

    def to_dict(self) -> dict:
        return {"code": self.code, "data": self.data}

    def __str__(self):
        return f"ResponseModel [{self.code}] data={self.data})"

    def __repr__(self):
        return f"ResponseModel (code={self.code}, data={self.data})"


class HTTPResponseModel(ResponseModel):
    def __init__(self, data: Dict[str, Any], status_code: int):
        self.status_code = status_code
        super().__init__(status_code, data)

    @property
    def status_code(self) -> int:
        return self._status_code

    @status_code.setter
    def status_code(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Status code must be an integer.")
        if value < 200 or value > 599:
            raise ValueError("Status code must be between 200 and 599.")
        self._status_code = value

    def to_dict(self) -> dict:
        return {"code": self.code, "data": self.data, "status_code": self.status_code}

    def __str__(self):
        return f"HTTPResponseModel [{self.status_code}] data={self.data})"

    def __repr__(self):
        return f"HTTPResponseModel (data={self.data}, status_code={self.status_code})"

    def to_http_response(self):
        return self.data, self.status_code


class HTTPResponseErrorModel(HTTPResponseModel):
    def __init__(self, err_code: ErrorCode, status_code: int, traceback: str = None, trace_id: str = None):
        self.err_code = err_code.value[0]
        self.message = err_code.value[1]
        self.traceback = traceback
        self.code = status_code
        self.trace_id = trace_id

    def to_dict(self) -> dict:
        return {"err_code": self.err_code, "message": self.message, 'traceback': self.traceback, "trace_id": self.trace_id}

    def __str__(self):
        return f"HTTPResponseErrorModel [{self.err_code}] data={self.data} trace_id={self.trace_id})"

    def __repr__(self):
        return f"HTTPResponseErrorModel (data={self.data}, status_code={self.code} trace_id={self.trace_id})"

    def to_http_response(self):
        return self.to_dict(), self.code
