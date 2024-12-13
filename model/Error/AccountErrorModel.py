
class AbstractAccountErrorModel:

    '''
    Error Model inherit from python built in Exception
    '''

    def __init__(self, exception: str, account_id: str, document_id: str,  occurred_at: str, trace_id: str) -> None:
        '''
        exception:str; account exception 
        account_id:str; account_id
        trace_id:str; trace_id
        occurred_at:str; time of error occurred in str format
        '''

        self.exception = exception
        self.account_id = account_id
        self.trace_id = trace_id
        self.occurred_at = occurred_at
        self.document_id = document_id

    def to_dict(self) -> dict:
        return {"exception": self.exception, "account": self.account_id, 'document_id': self.document_id, "trace_id": self.trace_id,
                "occurred_at": self.occurred_at}

    @staticmethod
    def from_dict(d: dict):
        model = AbstractAccountErrorModel(
            d.get('exception', 'empty exception'),
            d.get('account', 'empty account'),
            d.get('document_id', 'empty document_id'),
            d.get('occurred_at', 'empty occurred_at'),
            d.get('trace_id', 'empty trace_id'),)
        return model

    @property
    def exception(self):
        return self._exception

    @exception.setter
    def exception(self, value):
        if isinstance(value, str):
            self._exception = value
        else:
            raise Exception('Invalid value, the value must be str.')

    @property
    def trace_id(self):
        return self._trace_id

    @trace_id.setter
    def trace_id(self, value):
        if isinstance(value, str):
            self._trace_id = value
        else:
            raise Exception('Invalid value, the value must be str.')
