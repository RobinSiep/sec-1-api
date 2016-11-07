import logging
import transaction

from sec_1_api.models.meta import DBSession as session

log = logging.getLogger(__name__)


def commit():
    transaction.commit()


def expunge(instance):
    session.expunge(instance)


def persist(obj):
    session.add(obj)
    session.flush()
    return obj


def rollback():
    return session.rollback()
