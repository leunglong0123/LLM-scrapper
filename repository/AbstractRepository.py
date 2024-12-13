import os
import abc
import os
import logging
import traceback
from typing import List, Union
from google.cloud import bigquery

from sqlalchemy import text
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from model.Abstract import AbstractModel
from model.Error.AbstractErrorModel import AbstractErrorModel, ErrorCode
from model.common.QueryModel import CompoundQueryModel, QueryPaginationModel
from model.common.PaginateMetadata import PaginateMetadata
from model.common.Response import ResponseModel
from entity.AbstractPost import AbstractPostEntity

from dotenv import load_dotenv


load_dotenv()
logging.getLogger().setLevel(logging.INFO)
client = bigquery.Client()
GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
DATASET_ID = os.environ.get('DATASET_ID')
# TODO change into env variable


engine = create_engine(f'bigquery://{GCP_PROJECT_ID}',
                       execution_options={'http_proxy': None, 'http_proxy': None}, arraysize=500)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

schema = [
    bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("post_type", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("likes", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("comments", "INT64", mode="REQUIRED"),
    bigquery.SchemaField("is_video", "BOOL", mode="REQUIRED"),
    bigquery.SchemaField("owner_username", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("caption_hashtags", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("caption", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("batch_id", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("url", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("shortcode", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("label_annotations", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("context", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("label_list", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("fetched_by", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("uploaded_at", "DATETIME", mode="REQUIRED"),
    bigquery.SchemaField("created_at", "DATETIME", mode="REQUIRED"),
    bigquery.SchemaField("updated_at", "DATETIME", mode="REQUIRED")
]


class AbstractRepository():
    '''
    set_one(entity: AbstractAccount) -> None
    set_many(items: list[dict]) -> None
    get_one(doc_id: AnyStr) -> 'AbstractAccount'
    get_many(self, field: str, operand: str, value, order_field: str = None, orderby: str = 'asc', ) -> list[AnyStr]:
    update(id: AnyStr, entity: AbstractAccount) -> None
    delete(self, doc_id: str) -> None
    '''

    def __init__(self, table_id, schema):
        self.dataset_id = DATASET_ID
        self.table_id = table_id
        self.client = client
        self.logging = logging
        self.entity = AbstractPostEntity
        self.schema = schema
        self.project_id = GCP_PROJECT_ID
        self.create_data_set_if_not_exist(
            self.dataset_id)
        self.table_ref = self.create_table_if_not_exist(
            self.table_id, self.schema)

    def create_data_set_if_not_exist(self, dataset_id) -> None:
        try:
            self.client.get_dataset(dataset_id)
            self.logging.info(f"Dataset {dataset_id} exists.")
        except Exception as e:
            try:
                self.client.create_dataset(dataset_id)
                self.logging.info(f"Dataset {dataset_id} created.")
            except Exception as e:
                self.logging.error(AbstractErrorModel(
                    ErrorCode.ABS_ERR_DB, traceback.format_exc()).to_dict())
                raise e

    def create_table_if_not_exist(self, table_id: str, schema: list) -> Table:
        try:
            if table_id is None:
                raise ValueError("Table id is None")
            if schema is None:
                raise Exception(f"Table {table_id} Have no schema")
            table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
            try:
                res = self.client.get_table(table_ref)
                self.logging.info(f"Table {table_ref} exists.")
                return res
            except:
                res = self.client.create_table(
                    bigquery.Table(
                        table_ref=table_ref,
                        schema=schema,
                    )
                )
                self.logging.info(f"Table {table_id} created.")
                return res
        except Exception as e:
            self.logging.error(AbstractErrorModel(
                ErrorCode.ABS_ERR_DB, traceback.format_exc()).to_dict())
            raise e

    @abc.abstractmethod
    def set_one(self, model: AbstractModel) -> AbstractModel:
        try:
            bq_session = Session()
            entity = model.to_entity()
            res = bq_session.add(entity)
            bq_session.commit()
            obj = bq_session.query(self.entity).get(entity.id)
            return obj
        except Exception as e:
            bq_session.rollback()
            self.logging.error(AbstractErrorModel(
                ErrorCode.ABS_ERR_CREATE, traceback.format_exc()).to_dict())
            raise e
        finally:
            bq_session.close()

    @abc.abstractmethod
    def set_many(self, models: List[AbstractModel]) -> None:
        try:
            bq_session = Session()
            entity_list = [post_model.to_entity() for post_model in models]
            res = bq_session.add_all(entity_list)
            bq_session.commit()
            return res
        except Exception as e:
            bq_session.rollback()
            self.logging.error(AbstractErrorModel(
                ErrorCode.ABS_ERR_CREATE, traceback.format_exc()).to_dict())
            raise e
        finally:
            bq_session.close()

    @abc.abstractmethod
    def get_one(self, id: str) -> Union[AbstractModel, None]:
        try:
            bq_session = Session()
            self.logging.info(f"Getting post with id {id}")
            res = bq_session.query(self.entity).get({'id': id})
            if res is None:
                return None
            return res.to_model()
        except Exception as e:
            self.logging.error(AbstractErrorModel(
                ErrorCode.ABS_ERR_READ, traceback.format_exc()).to_dict())
            raise e
        finally:
            Session.remove()

    @abc.abstractmethod
    def query(self, c_query_model: Union[CompoundQueryModel, QueryPaginationModel] = None, limit=100) -> ResponseModel:
        """
        query object e.g. ["id > 1", "likes < 10"], the clause will be textualized
        query_obj: list[str] = None, order_field: str = 'id', orderby: str = 'ASC',
        """
        try:
            bq_session = Session()
            stmt = bq_session.query(self.entity)

            if c_query_model.orderby:
                if c_query_model.is_asc:
                    stmt = stmt.order_by(
                        getattr(self.entity, c_query_model.orderby).asc())
                else:
                    stmt = stmt.order_by(
                        getattr(self.entity, c_query_model.orderby).desc())

            for clause in c_query_model.queries:
                stmt_clause = f'{clause.field} {clause.operator} {clause.value}'
                stmt = stmt.filter(text(stmt_clause))

            stmt = stmt.limit(limit)
            res = stmt.all()

            # pagination
            if isinstance(c_query_model, QueryPaginationModel):
                offset = (c_query_model.page_number - 1) * \
                    c_query_model.page_size
                stmt = stmt.limit(c_query_model.page_size).offset(offset)
                docs = stmt.all()
                paginate_metadata = PaginateMetadata(
                    data=[entity.to_model() for entity in docs],
                    page_number=c_query_model.page_number,
                    page_size=c_query_model.page_size,
                    total_items=len(res)
                )
                return ResponseModel(code=0, data=paginate_metadata)
            else:
                return ResponseModel(code=0, data=[entity.to_model() for entity in res])
        except Exception as e:
            self.logging.error(AbstractErrorModel(
                ErrorCode.ABS_ERR_READ, traceback.format_exc()).to_dict())
            raise e
        finally:
            Session.remove()

    @abc.abstractmethod
    def update(self, id: str, values: dict) -> AbstractModel:
        try:
            bq_session = Session()
            res = bq_session.query(self.entity).filter_by(id=id).update(values)
            bq_session.commit()
            self.logging.info(
                f"Updated post with id {id}, affected {res} rows.")
        except Exception as e:
            bq_session.rollback()
            self.logging.error(AbstractErrorModel(
                ErrorCode.ABS_ERR_UPDATE, traceback.format_exc()).to_dict())
            raise e
        finally:
            Session.remove()

    @abc.abstractmethod
    def update_with_filter(self, filter_values: dict, values: dict) -> AbstractModel:
        try:
            bq_session = Session()
            query = bq_session.query(self.entity)
            for field, value in filter_values.items():
                query = query.filter(getattr(self.entity, field) == value)

            count = query.count()

            if count > 1:
                self.logging.warning(
                    "Multiple records found with filters: {}".format(filter_values))
                # raise DuplicateRecordException("Multiple records found with filters: {}".format(filter_values))
            if count == 0:
                self.logging.warning(
                    "No records found with filters: {}".format(filter_values))
                return None
            res = query.one_or_none()
            updated = query.update(values)
            bq_session.commit()
            self.logging.info(f"Updated rows, affected {updated} rows.")

            res_model = res.to_model()
            self.logging.info(
                "Retrieved record with filters: {}".format(filter_values))
            return res_model
        except Exception as e:
            bq_session.rollback()
            self.logging.error(AbstractErrorModel(
                ErrorCode.ABS_ERR_UPDATE, traceback.format_exc()).to_dict())
            raise e
        finally:
            Session.remove()

    @abc.abstractmethod
    def delete(self, id: str) -> None:
        try:
            bq_session = Session()
            res = bq_session.query(self.entity).filter_by(id=id).delete()
            self.logging.info(
                f"Delete record with id {id}, affected {res} rows.")
            bq_session.commit()
            return res
        except Exception as e:
            bq_session.rollback()
            self.logging.error(AbstractErrorModel(
                ErrorCode.ABS_ERR_DELETE, traceback.format_exc()).to_dict())
            raise e
        finally:
            Session.remove()
