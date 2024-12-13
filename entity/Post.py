import os
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from google.cloud import bigquery

from dotenv import load_dotenv
load_dotenv()

INSTAGRAM_POST_TABLE = os.environ.get('INSTAGRAM_POST_TABLE')
DATASET_ID = os.environ.get('DATASET_ID')


Base = declarative_base()


class AbstractModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, nullable=False)

    def __init__(self, id=None):
        self.id = id


class AbstractPostEntity(AbstractModel):
    __abstract__ = True
    id = Column(String, primary_key=True, nullable=False)
    uploaded_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self, id=None, uploaded_at=None, created_at=None, updated_at=None):
        super().__init__(id=id)
        self.uploaded_at = uploaded_at
        self.created_at = created_at
        self.updated_at = updated_at


class InstagramPostEntity(AbstractPostEntity):
    __tablename__ = f'{DATASET_ID}.{INSTAGRAM_POST_TABLE}'
    post_type = Column(String)
    likes = Column(Integer)
    comments = Column(Integer)
    is_video = Column(Boolean)
    owner_username = Column(String)
    batch_id = Column(String)
    caption_hashtags = Column(String)
    caption = Column(String)
    url = Column(String)
    shortcode = Column(String)
    fetched_by = Column(String)
    label_annotations = Column(String, nullable=False)
    context = Column(String, nullable=False)
    label_list = Column(String, nullable=False)

    def __init__(self, id=None,
                 post_type=None,
                 uploaded_at=None, created_at=None, updated_at=None,
                 likes=None, comments=None, is_video=None, owner_username=None, batch_id=None,
                 caption_hashtags=None, caption=None, url=None, shortcode=None, fetched_by=None,
                 label_annotations=None, context=None, label_list=None):
        super().__init__(id=id, uploaded_at=uploaded_at,
                         created_at=created_at, updated_at=updated_at)
        self.post_type = post_type
        self.likes = likes
        self.comments = comments
        self.is_video = is_video
        self.owner_username = owner_username
        self.batch_id = batch_id
        self.caption_hashtags = caption_hashtags
        self.caption = caption
        self.url = url
        self.shortcode = shortcode
        self.fetched_by = fetched_by
        self.label_annotations = label_annotations
        self.context = context
        self.label_list = label_list

    def __repr__(self):
        return f"<InstagramPostEntity (shortcode={self.shortcode}, owner_username={self.owner_username}, created_at={self.created_at}), batch_id={self.batch_id}>"

    def to_model(self):
        from Model.Post import PostModel
        model = PostModel.from_entity(self)
        return model

    def to_dict(self):
        return {
            'id': self.id,
            'post_type': self.post_type,
            'uploaded_at': self.uploaded_at,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'likes': self.likes,
            'comments': self.comments,
            'is_video': self.is_video,
            'fetched_by': self.fetched_by,
            'owner_username': self.owner_username,
            'batch_id': self.batch_id,
            'caption_hashtags': self.caption_hashtags,
            'caption': self.caption,
            'url': self.url,
            'shortcode': self.shortcode,
            'label_annotations': self.label_annotations,
            'context': self.context,
            'label_list': self.label_list
        }
