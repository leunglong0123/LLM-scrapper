# metadata of pagination model
from typing import Any


class PaginateMetadata():
    def __init__(self, data: list[Any], page_number: int, page_size: int, total_items: int) -> None:
        self.data = data
        self.page_number = page_number
        self.page_size = page_size
        self.total_items = total_items
        self.has_next = total_items > page_size * page_number
        self.has_prev = page_number > 1
        pass

    def to_dict(self) -> dict:
        return {
            'data': [d.to_dict() for d in self.data],
            'page': self.page_number,
            'size': self.page_size,
            'total_items': self.total_items,
            'has_next': self.has_next,
            'has_prev': self.has_prev
        }

    def __str__(self) -> str:
        return (
            f"PaginateMetadata(data={self.data}, \n"
            f"  page_number={self.page_number}, \n"
            f"  page_size={self.page_size}, \n"
            f"  total_items={self.total_items}, \n"
            f"  has_next={self.has_next}, \n"
            f"  has_prev={self.has_prev})"
        )
