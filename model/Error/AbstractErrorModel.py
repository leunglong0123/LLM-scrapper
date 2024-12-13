import os
import sys
from enum import Enum
from types import TracebackType
from typing import Union
from google.cloud import logging
from dotenv import load_dotenv
import traceback
# 'ErrorCode.CONTROL_ERR_READ'
# use this pattern


class ErrorCode(Enum):
    OK = 0, 'success'
    ERR = -1, 'error'
    MODEL_ERR = 900, 'error in model layer'
    ABS_ERR_DB = 1005, 'error in database in abstract repository layer'
    ABS_ERR_CREATE = 1001, 'error in create in abstract repository layer'
    ABS_ERR_READ = 1002, 'error in read in abstract repository layer'
    ABS_ERR_UPDATE = 1003, 'error in update in abstract repository layer'
    ABS_ERR_DELETE = 1004, 'error in delete in abstract repository layer'
    REPOSITORY_ERR = 2000, 'error in repository layer'
    REPOSITORY_ERR_CREATE = 2001, 'error in create in repository layer'
    REPOSITORY_ERR_READ = 2002, 'error in read in repository layer'
    REPOSITORY_ERR_UPDATE = 2003, 'error in update in repository layer'
    REPOSITORY_ERR_DELETE = 2004, 'error in delete in repository layer'
    SERVICE_ERR = 3000, 'error in service layer'
    SERVICE_ERR_CREATE = 3001, 'error in create in service layer'
    SERVICE_ERR_READ = 3002, 'error in read in service layer'
    SERVICE_ERR_UPDATE = 3003, 'error in update in service layer'
    SERVICE_ERR_DELETE = 3004, 'error in delete in service layer'
    SERVICE_ERR_HANDLER = 3005, 'error in handler in service layer'
    SERVICE_ERR_NOT_FOUND = 3006, 'error in not found in service layer'
    SERVICE_MEDIA_GET_ERR = 3101, 'error in get media in service layer'
    SERVICE_MEDIA_PUT_ERR = 3102, 'error in put media in service layer'
    SERVICE_MEDIA_SERVER_DISCONNECTED = 3103, 'error in server disconnect  in service layer'
    SERVICE_INSTALOADER = 3200, 'error in instaloader in service layer'
    SERVICE_PROXY = 3300, 'error in proxy in service layer'
    SERVICE_PUBSUB = 3400, 'error in pubsub in service layer'
    SERVICE_JSON_DECODE = 3500, 'error in json decode in service layer'
    SERVICE_REDDIT = 3600, 'error in reddit in service layer'
    SERVICE_REDDIT_GET = 3601, 'error in reddit get in service layer'
    SERVICE_REDDIT_CREATE = 3602, 'error in reddit create in service layer'
    SERVICE_REDDIT_UPDATE = 3603, 'error in reddit update in service layer'
    SERVICE_REDDIT_DELETE = 3604, 'error in reddit delete in service layer'
    SERVICE_QUEUE_EMPTY = 3700, 'error in queue empty in service layer'
    SERVICE_QUEUE_FULL = 3701, 'error in queue full in service layer'
    SERVICE_THREAD_CREATION_FAILURE = 3800, 'error in thread creation in service layer'
    SERVICE_THREAD_START = 3801, 'error in thread start in service layer'
    SERVICE_THREAD_JOIN_FAILURE = 3802, 'error in thread join in service layer'
    CONTROL_ERR = 4000, 'error in control layer'
    CONTROL_ERR_CREATE = 4001, 'error in create in control layer'
    CONTROL_ERR_READ = 4002, 'error in read in control layer'
    CONTROL_ERR_UPDATE = 4003, 'error in update in control layer'
    CONTROL_ERR_DELETE = 4004, 'error in delete in control layer'
    CONTROL_ERR_INSTALOADER = 4100, 'error in instaloder in control layer'
    CONTROL_ERR_INSTALOADER_LOGIN = 4101, 'error in instaloder login in control layer'
    CONTROL_ERR_INSTALOADER_GET = 4102, 'error in instaloder get in control layer'
    CONTROL_ERR_INSTALOADER_DECODE_JSON = 4103, 'error in instaloder decode json in control layer'
    CONTROL_ERR_INSTALOADER_EOB_TXT = 4104, 'error in creating End of Batch Document in control layer'
    CONTROL_ERR_INSTALOADER_DECODE_RESPONSE = 4105, 'error in unpacking response in control layer'

    FLASK_ERR = 5000, 'error in flask application'
    FLASK_ERR_CREATE = 5001, 'error in create in flask application'
    FLASK_ERR_READ = 5002, 'error in read in flask application'
    FLASK_ERR_UPDATE = 5003, 'error in update in flask application'
    FLASK_ERR_DELETE = 5004, 'error in delete in flask application'
    ERR_HANDLER = 6000, 'error in handler in flask application'
    ERR_HANDLER_GET = 6001, 'error in handler in flask application'
    PUB_SUB_ERR = 7000, 'error in pubsub'
    INSTALOADER_ERR = 8000, 'error in installer'
    INSTALOADER_ERR_LOGIN = 8001, 'error in installer login'
    INSTALOADER_ERR_GET = 8002, 'error in installer get'
    INSTALOADER_ERR_PUT = 8003, 'error in installer put'


class AbstractErrorModel(Exception):

    '''
    Error Model inherit from python built in Exception
    '''

    def __init__(self, code: ErrorCode, traceback: TracebackType) -> None:
        '''
        status: INFO, WARNING, ERROR, CRITICAL
        code: error code, indicate which layer
        message: error message
        traceback: error traceback
        '''
        self.code, self.message = code.value
        self.traceback = traceback
        self.class_name = self.__class__.__name__
        self.caller_class = sys._getframe(
            1).f_locals["self"].__class__.__name__

    def set_msg(self, msg: str) -> None:
        self.message = msg

    def to_dict(self) -> dict:
        return {"status": self.code, "message": self.message, "class_name": self.__class__.__name__,
                "traceback": self.traceback}

    def to_http(self) -> dict:
        return {"status": self.code, "traceback": self.traceback}

    def __str__(self):
        return f"{self.caller_class}: [{self.code}] {self.message} | Traceback: {self.traceback}"

    def __repr__(self):
        return f"{self.caller_class} (code={self.code}, message='{self.message}', traceback={self.traceback})"

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        if isinstance(value, int) or isinstance(value, str):
            self._code = value
        else:
            raise Exception('Invalid value, the value must be int.')

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        if isinstance(value, str):
            self._message = value
        else:
            raise Exception('Invalid value, the value must be str.')

    @property
    def traceback(self):
        return self._traceback

    @traceback.setter
    def traceback(self, value):
        if isinstance(value, str):
            self._traceback = value
        else:
            raise Exception('Invalid value, the value must be str.')

    # @ property
    # def trace_id(self):
    #     return self._trace_id

    # @ trace_id.setter
    # def trace_id(self, value):
    #     if isinstance(value, str):
    #         self._trace_id = value
    #     else:
    #         raise Exception('Invalid value, the value must be str.')
