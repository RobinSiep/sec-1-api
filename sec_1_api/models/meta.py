import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

log = logging.getLogger(__name__)


class LineageBase(object):
    def set_lineage(self, parent, name, request=None):
        self.__name__ = name
        self.__parent__ = parent
        self.request = request
