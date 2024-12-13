import os
import traceback
from typing import List, Union
from google.cloud import bigquery
from model.Error.ErrorModel import ErrorModel, ErrorCode
from model.Abstract import AbstractModel
from service.logger_service import LoggerService
from repository.InstagramRepository import InstagramRepository
from typing import Optional


GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
DATASET_ID = os.environ.get('DATASET_ID')
TABLE_ID = os.environ.get('TABLE_ID')
INSTAGRAM_POST_TABLE = os.environ.get('INSTAGRAM_POST_TABLE')


client = bigquery.Client(project=GCP_PROJECT_ID)


class BigQueryService():
    def __init__(self) -> None:
        self.logger = LoggerService()
        self.repo = InstagramRepository()
        self.schema = [
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

    def set_one(self, model: AbstractModel, trace_id: str) -> Optional[dict]:
        """
        Insert a single record into the BigQuery table.

        Args:
            model (AbstractModel): The model to be inserted.
            trace_id (str): Trace ID for logging.

        Returns:
            Optional[dict]: Returns the error if an error occurs; otherwise None.
        """
        try:
            self.logger.set_trace_id(trace_id)

            # Convert the model to a dictionary
            row = model.to_entity().to_dict()

            table_ref = f"{DATASET_ID}.{INSTAGRAM_POST_TABLE}"

            errors = client.insert_rows_json(
                table_ref, [row], row_ids=None
            )

            if not errors:
                self.logger.info(f"Row with ID {row['id']} has been added.")
                return None  # No errors
            else:
                raise Exception(
                    f"Encountered errors while inserting the row: {errors}"
                )
        except Exception as e:
            self.logger.error(
                ErrorModel(
                    e.__class__.__name__,
                    ErrorCode.SERVICE_ERR_CREATE,
                    traceback.format_exc(),
                ).to_dict()
            )
            raise e

    def set_many(self, models: List[AbstractModel], trace_id: str) -> Union[None, List]:
        try:
            self.logger.set_trace_id(trace_id)
            rows = []
            for model in models:
                row = model.to_entity().to_dict()
                rows.append(row)

            table_ref = f'{DATASET_ID}.{INSTAGRAM_POST_TABLE}'
            errors = client.insert_rows(
                table_ref, rows, selected_fields=self.schema)
            if errors == []:
                self.logger.info(f"{len(rows)} rows have been added.")
            else:
                raise Exception(
                    "Encountered errors while inserting rows: {}".format(errors))
            return errors
        except Exception as e:
            self.logger.error(ErrorModel(e.__class__.__name__, ErrorCode.SERVICE_ERR_CREATE,
                              traceback.format_exc()).to_dict())
            raise e
