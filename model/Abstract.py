from dotenv import load_dotenv
import os
from dataclasses import dataclass
from datetime import datetime

load_dotenv()

DATE_FORMAT = os.getenv('DATE_FORMAT', '%Y-%m-%dT%H:%M:%S')


class AbstractModel():
    def __init__(self, created_at: datetime = datetime.now(), updated_at: datetime = datetime.now()):
        try:
            self._created_at = DatetimeModel(created_at)
            self.created_at = self._created_at.value
            self._updated_at = DatetimeModel(updated_at)
            self.updated_at = self._updated_at.value
        except Exception as e:
            raise e
            # TODO ErrorModel raise AbstractErrorModel(ErrorCode.MODEL_ERR, traceback.format_exc())

    @staticmethod
    def isBool(value):
        if isinstance(value, bool):
            return True
        raise Exception(
            'AbstractModel Err. Invalid value type {}, the value must be Bool.'.format(type(value)))

    @staticmethod
    def isInt(value):
        if isinstance(value, int):
            return True
        raise Exception(
            'AbstractModel Err. Invalid value type {}, the value must be Int.'.format(type(value)))

    @staticmethod
    def isStr(value):
        if isinstance(value, str):
            return True
        raise Exception(
            'AbstractModel Err. Invalid value type {}, the value must be Str.'.format(type(value)))

    @staticmethod
    def isList(value):
        if isinstance(value, list):
            return True
        raise Exception(
            'AbstractModel Err. Invalid value type {}, the value must be List.'.format(type(value)))

    @staticmethod
    def isDate(value):
        if isinstance(value, datetime):
            return True
        raise Exception(
            'AbstractModel Err. Invalid value type {}, the value must be Date.'.format(type(value)))

    def to_entity(self):
        raise NotImplementedError()

    def to_dict(self):
        raise NotImplementedError()


class DatetimeModel():
    def __init__(self, value: datetime = datetime.now()):
        self.value = value
        self.str = value.strftime(DATE_FORMAT)
        pass

    @staticmethod
    def from_dynamic(value: 'DatetimeWithNanoseconds'):
        model = DatetimeModel()
        model.value = datetime.fromtimestamp(value.timestamp())
        model.str = value.strftime(DATE_FORMAT)
        return model

    @staticmethod
    def from_str(value: str, format: str = DATE_FORMAT):
        model = DatetimeModel()
        model.value = datetime.strptime(value, format)
        model.str = value
        return model

    def __repr__(self) -> str:
        return f"<DatetimeModel {self.value}>"

    @property
    def str(self):
        return self._str

    @str.setter
    def str(self, e):
        if isinstance(e, str):
            self._str = e

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, e):
        if isinstance(e, datetime):
            self._value = e
