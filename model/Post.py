from model.Abstract import AbstractModel, DatetimeModel
from entity.Post import InstagramPostEntity
from datetime import datetime
from typing import Optional, List


class PostModel(AbstractModel):
    def __init__(
        self,
        id: Optional[str] = None,
        post_type: Optional[str] = None,
        likes: Optional[int] = None,
        comments: Optional[int] = None,
        is_video: Optional[bool] = None,
        owner_username: Optional[str] = None,
        batch_id: Optional[str] = None,
        caption_hashtags: Optional[str] = None,
        caption: Optional[str] = None,
        url: Optional[str] = None,
        shortcode: Optional[str] = None,
        fetched_by: Optional[str] = None,
        uploaded_at: Optional[datetime] = datetime.now(),
        created_at: Optional[datetime] = datetime.now(),
        updated_at: Optional[datetime] = datetime.now(),
        label_annotations: Optional[List[str]] = None,
        context: Optional[str] = None,
        label_list: Optional[List[str]] = None
    ):
        self._id = id
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
        self._uploaded_at = DatetimeModel(uploaded_at)
        self.uploaded_at = self._uploaded_at.value
        self.label_annotations = label_annotations
        self.context = context
        self.label_list = label_list
        super().__init__(created_at, updated_at)

    # TODO - implement @properties decorator to getter and setter
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, str):
            self._id = value
        else:
            raise Exception('Invalid value, the value must be str.')

    def to_dict(self):
        return {
            "id": self.id,
            "post_type": self.post_type,
            "likes": self.likes,
            "comments": self.comments,
            "is_video": self.is_video,
            "owner_username": self.owner_username,
            "batch_id": self.batch_id,
            "caption_hashtags": self.caption_hashtags,
            "caption": self.caption,
            "url": self.url,
            "shortcode": self.shortcode,
            "fetched_by": self.fetched_by,
            "uploaded_at": self._uploaded_at.value,
            "created_at": self._created_at.value,
            "updated_at": self._updated_at.value,
            "label_annotations": self.label_annotations,
            "context": self.context,
            "label_list": self.label_list
        }

    @staticmethod
    def from_dict(data):
        model = PostModel(
            id=data['id'],
            post_type=data['post_type'],
            likes=data['likes'],
            comments=data['comments'],
            is_video=data['is_video'],
            owner_username=data['owner_username'],
            batch_id=data['batch_id'],
            caption_hashtags=data['caption_hashtags'],
            caption=data['caption'],
            url=data['url'],
            shortcode=data['shortcode'],
            fetched_by=data['fetched_by'],
            uploaded_at=data['uploaded_at'],
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            label_annotations=data['label_annotations'],
            context=data['context'],
            label_list=data['label_list']
        )
        return model

    @staticmethod
    def from_entity(entity: InstagramPostEntity):
        model = PostModel(
            id=entity.id,
            post_type=entity.post_type,
            likes=entity.likes,
            comments=entity.comments,
            is_video=entity.is_video,
            owner_username=entity.owner_username,
            batch_id=entity.batch_id,
            caption_hashtags=entity.caption_hashtags,
            caption=entity.caption,
            url=entity.url,
            shortcode=entity.shortcode,
            fetched_by=entity.fetched_by,
            uploaded_at=entity.uploaded_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            label_annotations=entity.label_annotations,
            context=entity.context,
            label_list=entity.label_list
        )
        return model

    def to_entity(self):
        entity = InstagramPostEntity(
            id=self.id,
            post_type=self.post_type,
            likes=self.likes,
            comments=self.comments,
            is_video=self.is_video,
            owner_username=self.owner_username,
            batch_id=self.batch_id,
            caption_hashtags=self.caption_hashtags,
            caption=self.caption,
            url=self.url,
            fetched_by=self.fetched_by,
            shortcode=self.shortcode,
            uploaded_at=self._uploaded_at.str,
            created_at=self._created_at.str,
            updated_at=self._updated_at.str,
            label_annotations=self.label_annotations,
            context=self.context,
            label_list=self.label_list
        )
        return entity

    def __repr__(self):
        return f"<PostModel (shortcode={self.shortcode}, created_at={self.created_at})>"
