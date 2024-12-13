import os
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from google.cloud import bigquery

from dotenv import load_dotenv
load_dotenv()

TEST_TABLE = os.environ.get('TEST_TABLE')
DATASET_ID = os.environ.get('DATASET_ID')
Base = declarative_base()


class AbstractModel(Base):
    __abstract__ = True
    __tablename__ = f'{DATASET_ID}.{TEST_TABLE}'
    id = Column(Integer, primary_key=True, nullable=False)


class AbstractPostEntity(AbstractModel):
    id = Column(String, primary_key=True, nullable=False)
    uploaded_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<AbstractPostEntity (uploaded_at={self.uploaded_at}, created_at={self.created_at}, created_at={self.created_at}), updated_at={self.updated_at}>"
