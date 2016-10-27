import logging

from marshmallow import ValidationError
from pyramid.httpexceptions import (HTTPBadRequest, HTTPInternalServerError,
                                    HTTPCreated)
from pyramid.view import view_config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, Content, Mail
from sqlalchemy.orm.exc import NoResultFound

from sec_1_api.lib.captcha import (google_recaptcha, increment_retries,
                                   captcha_needed, invalidate_retry_count)
from sec_1_api.lib.factories.root import RootFactory
from sec_1_api.lib.redis import RedisSession
from sec_1_api.lib.security import hash_password, get_secure_token
from sec_1_api.lib.validation.auth import RegisterSchema
from sec_1_api.lib.validation.user import SendRecoverSchema, RecoverSchema
from sec_1_api.models import commit, persist, rollback
from sec_1_api.models.user import User, get_user_by_email

log = logging.getLogger(__name__)


@view_config(permission='public', context=RootFactory, renderer='json',
             request_method='POST', name='register')
def post_user(request):
    # Check captcha as early as possible
    google_recaptcha(request)

    try:
        result, errors = RegisterSchema(strict=True).load(request.json_body)
    except ValidationError as e:
        raise HTTPBadRequest(json_body=e.messages)

    password_hash, password_salt = hash_password(result['password'])

    user = User(username=result['username'], password_hash=password_hash,
                password_salt=password_salt)

    if result["email"]:
        user.email = result["email"]

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
    try:
        result, errors = RecoverSchema(strict=True).load(request.json_body)
    except ValidationError as e:
        raise HTTPBadRequest(json_body=e.messages)

    # Check if a captcha is needed. The identifier is the email address in this
    # case. Otherwise an attack will be able to deduct if the email is stored
    # in the database by whether or not a recaptcha will appear after several
    # retries.
    increment_retries('recovery', request, result["email"])
    if captcha_needed('recovery', request, result["email"]):
        google_recaptcha(request)

    try:
        user = get_user_by_email(result["email"])
    except NoResultFound:
        return

    if _check_recover_code(user, result['recovery_code']):
        password_hash, password_salt = hash_password(result['password'])
        user.password_hash = password_hash
        user.password_salt = password_salt

        try:
            persist(user)
            invalidate_retry_count('recovery', request, result["email"])
        except:
            log.critical("Something went wrong updating the user",
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()
            return

    raise HTTPBadRequest(json_body={"recovery_code": "Invalid recovery code"})


@view_config(permission='public', context=RootFactory, renderer='json',
             request_method='POST', name='sendrecover')
def sendRecover(request):
    try:
        result, errors = SendRecoverSchema(strict=True).load(request.json_body)
    except ValidationError as e:
        raise HTTPBadRequest(json_body=e.messages)

    try:
        user = get_user_by_email(result["email"])
    except NoResultFound:
        return

    log.info("reached")

    increment_retries("send_recover", request, result["email"])

    if captcha_needed("send_recover", request, result["email"]):
        google_recaptcha(request)

    code = get_secure_token(8)

    _cache_recover_code(user, code)

    sendgridClient = SendGridAPIClient(
        apikey=request.registry.settings['sendgrid_api_key'])
    from_email = Email("noreply@localhost.com")
    subject = "Your recovery code"
    to_email = Email(result['email'])
    content = Content("text/plain", code)
    mail = Mail(from_email, subject, to_email, content)
    response = sendgridClient.client.mail.send.post(request_body=mail.get())
    if not response.status_code != 200:
        raise HTTPInternalServerError

    invalidate_retry_count('send_recover', request, result["email"])


def _cache_recover_code(user, code):
    # expire in 6 hours
    RedisSession().session.setex("recover_{}".format(user.id),
                                 21600, code)


def _check_recover_code(user, code):
    cached_recovery_code = RedisSession().session.get(
        "recover_{}".format(user.id))

    if (not cached_recovery_code or
            code != cached_recovery_code.decode('utf-8')):
        return False

    return True


@view_config(permission='public', context=RootFactory, name='signup',
             renderer='sec_1_api:templates/register.mako',
             request_method='GET')
def signup_view(request):
    return {}


@view_config(permission='public', context=RootFactory, request_method='GET',
             renderer='sec_1_api:templates/recover.mako', name='recover')
def recover_view(request):
    return {
        "send_captcha": captcha_needed("send_recover", request),
        "recovery_captcha": captcha_needed("recovery", request)
    }
