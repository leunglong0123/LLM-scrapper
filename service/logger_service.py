import os
import json
import traceback
import logging
import logging.config

from dotenv import load_dotenv
from google.cloud import logging as cloud_logging

# attempting separate logging service
load_dotenv()

# logging_client = cloud_logging.Client()
# logging_client.setup_logging()
logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOGGING_LEVEL"))
env = os.getenv("ENVIRONMENT")


class LoggerService():
    def __init__(self) -> None:
        self.logger = logger

    def setLevel(self, level: str):
        '''
        'CRITICAL': CRITICAL,
        'FATAL': FATAL,
        'ERROR': ERROR,
        'WARN': WARNING,
        'WARNING': WARNING,
        'INFO': INFO,
        'DEBUG': DEBUG,
        'NOTSET': NOTSET,
        '''
        self.logger.setLevel(level)

    def set_trace_id(self, trace_id: str):
        try:
            if trace_id == None:
                raise Exception("No trace_id attached")
            self._trace_id = trace_id
        except Exception as e:
            self.logger.error(
                {'trace_id': "No trace_id attached", 'log': traceback.format_exc()})

    def info(self, text: str) -> None:
        self.logger.info({'trace_id': self._trace_id, 'log': text})

    def error(self, text: str) -> None:
        log_message = {'trace_id': self._trace_id, 'log': json.dumps(
            str(text)).replace("\\n", " ").replace("\\", " ")}
        if env == "LOCAL":
            print(log_message)
        else:
            self.logger.error(log_message)

    def debug(self, *args, **kwargs) -> None:
        self.logger.debug(str({'trace_id': self._trace_id, 'log': {
                          'args': args, 'kwargs': kwargs}}))

    def warning(self, text: str) -> None:
        self.logger.warning({'trace_id': self._trace_id, 'log': text})
