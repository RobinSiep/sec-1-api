import logging
import uuid

from sqlalchemy import (Column, String, ForeignKey, Boolean, Table,
                        UniqueConstraint, PrimaryKeyConstraint)
from sqlalchemy.orm import backref, relationship

from sec_1_api.lib.security import get_secure_token
from sec_1_api.models.meta import UUID, Base, DBSession as session

log = logging.getLogger(__name__)


class Device(Base):
    __tablename__ = 'device'

    link_id = Column(
        String(24), primary_key=True, default=get_secure_token(16))
    secret_identifier = Column(String(24), unique=True)
    name = Column(String(250))
    on = Column(Boolean())
    pattern = Column(String(100))

    users = relationship('User', secondary=device_user,
                         backref=backref("devices", lazy="dynamic"))

    UniqueConstraint('name', 'user.id')


def get_device_by_link_id(link_id):
    return session.query(Device).filter(Device.link_id == link_id).one()


def get_device_by_secret_identifier(secret_identifier):
    return session.query(Device).filter(
        Device.secret_identifier == secret_identifier).one()


def get_devices_by_user_id(user_id):
    return session.query(Device).filter(Device.users.any(
        id=user_id)).all()
