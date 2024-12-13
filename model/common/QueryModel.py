from datetime import datetime
from firebase_admin import firestore
import traceback


class QueryModel():
    '''
    Use for Firestore CompoundQuery
    '''

    def __init__(self, field: str, operator: str, value: any) -> None:
        self.field = field
        self.operator = operator
        self.value = self.format_clause_value(value)

    def format_clause_value(self, value: str):
        if (value):
            if value.isdigit():
                return int(value)
            if value == 'True' or value == 'true':
                return True
            if value == 'False' or value == 'false':
                return False
        return value

    @property
    def operator(self) -> str:
        return self._operator

    @operator.setter
    def operator(self, operator: str) -> None:
        if operator not in ['<', '<=', '>', '>=', '==', '!=', 'in', 'not in', '=', 'IS']:
            raise ValueError(f'Invalid operator: {operator}')
        self._operator = operator

    def to_dict(self) -> dict:
        return {
            'field': self.field,
            'operator': self.operator,
            'value': self.value
        }

    @staticmethod
    def from_dict(d: dict):
        return QueryModel(d['field'], d['operator'], d['value'])

    def __str__(self) -> str:
        return f"QueryModel(field={self.field}, operator={self.operator}, value={self.value})"

    def __repr__(self) -> str:
        return f"QueryModel(field={self.field}, operator={self.operator}, value={self.value})"


class CompoundQueryModel():
    '''
    Chained Query Model
    '''

    def __init__(self, orderby=None, is_asc=False, limit=None) -> None:
        self.queries = []
        self.orderby = orderby
        self.is_asc = is_asc
        self.limit = limit
        self.is_pagination = False

    # writer setter of queries so it must be a list of QueryModel with length >  0
    @property
    def queries(self) -> list[QueryModel]:
        return self._queries

    @queries.setter
    def queries(self, queries: list[QueryModel]) -> None:
        # if len(queries) == 0:
        #     raise ValueError(f'Invalid queries: {queries}')
        # queries must be list
        if not isinstance(queries, list):
            raise ValueError(f'Invalid queries: {queries}')
        self._queries = queries

    def append(self, query: QueryModel) -> None:
        self.queries.append(query)

    def to_dict(self) -> dict:
        return {
            'queries': [query.to_dict() for query in self.queries],
            'orderby': self.orderby,
            'is_asc': self.is_asc
        }


class QueryPaginationModel(CompoundQueryModel):
    def __init__(self, page_number: int, page_size: int, orderby='created_at', is_asc=False) -> None:
        super().__init__(orderby, is_asc, page_size)
        self.page_number = page_number
        self.page_size = page_size
        self.is_pagination = True
