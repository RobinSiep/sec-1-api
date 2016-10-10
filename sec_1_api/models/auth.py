import logging
import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from sec_1_api.lib.security import get_secure_token
from sec_1_api.models.meta import Base

log = logging.getLogger(__name__)


class OAuthToken(Base):
    __tablename__ = 'oauth_token'
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUIDType(binary=False), ForeignKey('user.id'))
    token = Column(String(64), default=get_secure_token, unique=True)
    token_type = Column(Enum("Bearer", "Refresh", default="Bearer"))
    expiry_data = Column(DateTime)

    user = relationship('User')
