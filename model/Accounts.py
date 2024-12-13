import os
from datetime import datetime
from Model.Abstract import DatetimeModel
from Model.AbstractAccount import AbstractAccount
from Model.AccountSession import AccountSessionModel
from Model.Enums.Country import CountryEnum
DATETIME_FORMAT = os.environ.get('DATETIME_FORMAT')


class AccountModel(AbstractAccount):
    '''
    Account Model Extend from Base Model
    '''

    def __init__(self, id: str, username: str, pwd: str, status: str,
                 enabled: bool = True, is_authenticated: bool = False,
                 is_occupied: bool = False,
                 last_login_dt: datetime = datetime.now(),
                 login_attempt_count: int = 0, login_count: int = 0, post_scrapped_count: int = 0,
                 session_cookies: AccountSessionModel = None,
                 location: CountryEnum = None,
                 created_at: datetime = datetime.now(),
                 updated_at: datetime = datetime.now()
                 ) -> None:
        self.id = id
        self._last_login_dt = DatetimeModel(last_login_dt)
        self.last_login_dt = self._last_login_dt.value
        self._session_cookies = session_cookies if isinstance(
            session_cookies, AccountSessionModel) else None
        self.session_cookies = self._session_cookies.value if session_cookies else None
        super().__init__(username, pwd, status, enabled, is_authenticated, is_occupied,
                         login_attempt_count, login_count, post_scrapped_count, location, created_at, updated_at)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def last_login_dt(self):
        return self._last_login_dt.value

    @last_login_dt.setter
    def last_login_dt(self, value):
        self._last_login_dt = DatetimeModel(value)

    def to_dict(self):
        d = super().to_dict()
        d['id'] = self.id
        d['location'] = self.location.name if self.location else None
        d['last_login_dt'] = self._last_login_dt.value
        d['session_cookies'] = self._session_cookies.value if self.session_cookies else None
        return d

    @staticmethod
    def from_dict(d: dict):
        model = AccountModel(
            id=d['id'],
            username=d['username'],
            pwd=d['pwd'],
            status=d['status'],
            enabled=d['enabled'],
            is_authenticated=d['is_authenticated'],
            is_occupied=d['is_occupied'],
            last_login_dt=DatetimeModel.from_dynamic(
                d.get('last_login_dt', datetime.now())).value,
            login_attempt_count=d['login_attempt_count'],
            login_count=d['login_count'],
            post_scrapped_count=d['post_scrapped_count'],
            location=CountryEnum[d['location']] if d.get(
                'location', None) else None,
            session_cookies=AccountSessionModel(session_cookies=d.get(
                'session_cookies', None), account_id=d['id'], username=d['username']),
            created_at=d['created_at'],
            updated_at=d['updated_at']
        )
        return model

    def __eq__(self, other):
        if isinstance(other, AccountModel):
            if other.id == self.id and other.username == self.username and other.pwd == self.pwd and other.status == self.status and other.enabled == self.enabled and other.is_authenticated == self.is_authenticated and other.is_occupied == self.is_occupied and other.last_login_dt == self.last_login_dt and other.login_attempt_count == self.login_attempt_count and other.login_count == self.login_count and other.location == self.location:
                return True
        return False

    def __str__(self):
        return (
            f"AccountModel(\n"
            f"    username={self.username},\n"
            f"    status={self.status},\n"
            f"    enabled={self.enabled}\n"
            f")"
        )

    def __repr__(self):
        return (
            f"AccountModel(\n"
            f"    id={self.id},\n"
            f"    username={self.username},\n"
            f"    pwd={self.pwd},\n"
            f"    status={self.status},\n"
            f"    enabled={self.enabled},\n"
            f"    is_authenticated={self.is_authenticated},\n"
            f"    is_occupied={self.is_occupied},\n"
            f"    last_login_dt={self.last_login_dt},\n"
            f"    login_attempt_count={self.login_attempt_count},\n"
            f"    login_count={self.login_count},\n"
            f"    post_scrapped_count={self.post_scrapped_count},\n"
            f"    session_cookies={self.session_cookies},\n"
            f"    location={self.location},\n"
            f"    created_at={self.created_at},\n"
            f"    updated_at={self.updated_at}\n"
            f")"
        )
