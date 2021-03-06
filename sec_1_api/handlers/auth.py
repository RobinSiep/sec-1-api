import logging

from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPOk, HTTPBadRequest
from pyramid.security import forget, remember
from pyramid.view import view_config
from sqlalchemy.orm.exc import NoResultFound

from sec_1_api.lib.captcha import (google_recaptcha, increment_retries,
                                   captcha_needed, invalidate_retry_count)
from sec_1_api.lib.factories.root import RootFactory
from sec_1_api.lib.security import check_password
from sec_1_api.lib.validation.auth import LoginSchema
from sec_1_api.models.user import get_user_by_username

log = logging.getLogger(__name__)


@view_config(context=RootFactory, permission='public', renderer='json',
             request_method="POST", name="login")
def login(request):

    try:
        result, errors = LoginSchema(strict=True).load(request.json_body)
    except ValidationError as e:
        raise HTTPBadRequest(json_body=e.messages)

    increment_retries('login', request, result["username"])
    if captcha_needed('login', request, result["username"]):
        google_recaptcha(request)

    try:
        user = get_user_by_username(username=result["username"])
    except NoResultFound:
        check_password(result["password"])
        raise HTTPBadRequest(
            json={"password": "Username and password don't match"})

    check_password(result["password"], user.password_hash, user.password_salt)

    headers = remember(request, str(user.id))

    invalidate_retry_count('login', request, result["username"])

    # Return the session cookie
    return request.response.headerlist.extend(headers)


@view_config(context=RootFactory, permission='logout', name='logout',
             renderer='json', request_method='GET')
def logout(request):
    request.session.invalidate()
    return HTTPOk(headers=forget(request))
