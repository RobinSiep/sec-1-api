import logging

from marshmallow import ValidationError
from pyramid.httpexceptions import (HTTPBadRequest, HTTPInternalServerError,
                                    HTTPCreated)
from pyramid.view import view_config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, Content, Mail

from sec_1_api.lib.factories.root import RootFactory
from sec_1_api.lib.security import hash_password
from sec_1_api.lib.validation.auth import RegisterSchema
from sec_1_api.lib.validation.user import SendRecoverSchema, RecoverSchema
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


@view_config(permission='public', context=RootFactory, renderer='json',
             request_method='POST', name='sendrecover')
def sendRecover(request):
    try:
        result, errors = SendRecoverSchema(strict=True).load(request.json_body)
    except ValidationError as e:
        raise HTTPBadRequest(json_body=e.messages)

    sendgridClient = SendGridAPIClient(
        apikey=request.registry.settings['sendgrid_api_key'])
    from_email = Email("noreply@localhost.com")
    subject = "Your recovery code"
    to_email = result['email']
    content = Content("text/plain", "recoverdcode")
    mail = Mail(from_email, subject, to_email, content)
    response = sendgridClient.mail.send.post(request_body=mail.get())
    if not response.status_code != 200:
        raise HTTPInternalServerError


@view_config(permission='public', context=RootFactory, name='signup',
             renderer='sec_1_api:templates/register.mako',
             request_method='GET')
def signup_view(request):
    return {}


@view_config(permission='public', context=RootFactory, request_method='GET',
             renderer='sec_1_api:templates/recover.mako', name='recover')
def recover_view(request):
    return {}
