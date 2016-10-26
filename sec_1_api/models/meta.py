import logging
import uuid

from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.types import TypeDecorator
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

log = logging.getLogger(__name__)


class LineageBase(object):
    def set_lineage(self, parent, name, request=None):
        self.__name__ = name
        self.__parent__ = parent
        self.request = request


class UUID(TypeDecorator):
    impl = String

    # unused argumennt for alembic autogenerate
    def __init__(self, length=None):
        self.impl.length = 36
        super().__init__(length=self.impl.length)

    def process_bind_param(self, value, dialect=None):
        if value and isinstance(value, uuid.UUID):
            return str(value)
        elif value and not isinstance(value, uuid.UUID):
            try:
                return str(uuid.UUID(value))
            except:
                raise ValueError('value {} is not a valid UUID'.format(value))
        else:
            return None

    def process_result_value(self, value, dialect=None):
        if not value:
            return None
        try:
            if isinstance(value, str):
                value = value.strip()
            return uuid.UUID(value)
        except ValueError:
            raise

    def is_mutable(self):
        return False
