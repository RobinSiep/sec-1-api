import logging
import uuid

from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType

from sec_1_api.models.meta import Base, DBSession as session

log = logging.getLogger(__name__)


class User(Base):
    __tablename__ = 'user'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), unique=True)
    password_hash = Column(String(100))
    password_salt = Column(String(100))


def get_user_by_username(username):
    return session.query(User).filter(User.username == username).one()
