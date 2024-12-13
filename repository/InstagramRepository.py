import os
from typing import List

from google.cloud import bigquery

from typing import Union
from model.Post import PostModel
from model.Error.ErrorModel import ErrorModel
from model.common.QueryModel import QueryPaginationModel, CompoundQueryModel
from model.common.Response import ResponseModel
from entity.Post import InstagramPostEntity
from repository.AbstractRepository import AbstractRepository

from dotenv import load_dotenv
load_dotenv()
INSTAGRAM_POST_TABLE = os.environ.get('INSTAGRAM_POST_TABLE')
GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
DATASET_ID = os.environ.get('DATASET_ID')
# TODO change into env variable


class InstagramRepository(AbstractRepository):
    '''
    set_one(entity: AbstractAccount) -> None
    set_many(items: list[dict]) -> None
    get_one(doc_id: AnyStr) -> 'AbstractAccount'
    get_many(self, field: str, operand: str, value, order_field: str = None, orderby: str = 'asc', ) -> list[AnyStr]:
    update(id: AnyStr, entity: AbstractAccount) -> None
    delete(self, doc_id: str) -> None
    '''

    def __init__(self):
        schema = [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("post_type", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("likes", "INT64", mode="REQUIRED"),
            bigquery.SchemaField("comments", "INT64", mode="REQUIRED"),
            bigquery.SchemaField("is_video", "BOOL", mode="REQUIRED"),
            bigquery.SchemaField("owner_username", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("caption_hashtags",
                                 "STRING", mode="REQUIRED"),
            bigquery.SchemaField("caption", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("batch_id", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("url", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("shortcode", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("label_annotations",
                                 "STRING", mode="NULLABLE"),
            bigquery.SchemaField("context", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("label_list", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("fetched_by", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("uploaded_at", "DATETIME", mode="REQUIRED"),
            bigquery.SchemaField("created_at", "DATETIME", mode="REQUIRED"),
            bigquery.SchemaField("updated_at", "DATETIME", mode="REQUIRED")
        ]
        super().__init__(INSTAGRAM_POST_TABLE, schema)
        self.entity = InstagramPostEntity

    def create_data_set_if_not_exist(self, dataset_id) -> None:
        return super().create_data_set_if_not_exist(dataset_id)

    def create_table_if_not_exist(self, table_id: str, schema: list) -> None:
        return super().create_table_if_not_exist(table_id, schema)

    def set_one(self, post_model: PostModel) -> PostModel:
        return super().set_one(post_model)

    def set_many(self, post_model_list: List[PostModel]) -> None:
        return super().set_many(post_model_list)

    def get_one(self, id: str) -> PostModel:
        return super().get_one(id)

    def query(self, query_obj: Union[QueryPaginationModel, CompoundQueryModel]) -> ResponseModel:
        return super().query(query_obj)

    def update(self, id: str, values: dict) -> PostModel:
        return super().update(id, values)

    def delete(self, id: str) -> None:
        return super().delete(id)
