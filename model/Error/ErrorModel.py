from enum import Enum
from types import TracebackType
from typing import Union
from google.cloud import logging
from dotenv import load_dotenv
from model.Error.AbstractErrorModel import AbstractErrorModel
from model.Error.AbstractErrorModel import ErrorCode

# self__class__.__name__

load_dotenv()

__all__ = [
    'ErrorCode'
]


class ErrorModel(AbstractErrorModel):
    def __init__(self, cls: str,  code: Enum, traceback: TracebackType) -> None:
        super().__init__(code, traceback)
        self.caller_class = cls

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, code: Union[str, int]) -> None:
        self._code = code

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()
