import logging

from marshmallow import ValidationError
from pyramid.httpexceptions import (HTTPBadRequest, HTTPInternalServerError,
                                    HTTPCreated)
from pyramid.view import view_config

from sec_1_api.lib.factories.root import RootFactory
from sec_1_api.lib.security import hash_password
from sec_1_api.lib.validation.auth import RegisterSchema
from sec_1_api.models import commit, persist, rollback
from sec_1_api.models.user import User

log = logging.getLogger(__name__)


@view_config(permission='public', context=RootFactory, renderer='json',
             request_method='POST', name='register')
def post_user(request):
    try:
        result, errors = RegisterSchema(strict=True).load(request.json_body)
    except ValidationError as e:
        raise HTTPBadRequest(json_body=e.messages)

    password_hash, password_salt = hash_password(result['password'])

    user = User(username=result['username'], password_hash=password_hash,
                password_salt=password_salt)

    try:
        persist(user)
    except:
        log.critical("Something went wrong saving the user", exc_info=True)
        rollback()
        raise HTTPInternalServerError
    finally:
        commit()

    raise HTTPCreated


@view_config(permission='public', context=RootFactory, renderer='json',
             request_method='POST', name='recover')
def recovery(request):
    return {}


@view_config(permission='public', context=RootFactory, name='signup',
             renderer='sec_1_api:templates/register.mako',
             request_method='GET')
def signup_view(request):
    return {}


@view_config(permission='public', context=RootFactory, request_method='GET',
             renderer='sec_1_api:templates/recover.mako', name='recover')
def recover_view(request):
    return {}
