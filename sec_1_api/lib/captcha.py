import logging
import requests
from pyramid.httpexceptions import HTTPBadRequest

from sec_1_api.lib.redis import RedisSession

log = logging.getLogger(__name__)


def google_recaptcha(request):
    recaptcha_response = request.json_body.get('g-recaptcha-response')
    settings = request.registry.settings
    url = settings['google_recaptcha.url']
    data = {
        "secret": settings['google_recaptcha.secret'],
        "response": recaptcha_response,
        "remoteip": request.client_addr
    }
    response = requests.post(url, data)
    if response.json()['success']:
        return
    raise HTTPBadRequest(json_body={"g-recaptcha": "Invalid captcha given"})


def captcha_needed(context, request, identifier=None):
    needed = True
    # In case of a mako template render handler no identifier will be supplied
    # only the client addr will be checked to allow the front-end to determine
    # whether it should show the captcha. Keep in mind an identifier will have
    # to be supplied when dealing with resource mutations
    if identifier:
        retry_count = _get_retry_count(context, identifier)
    else:
        retry_count = 0

    client_addr_retry_count = _get_retry_count(context, request.client_addr)

    if retry_count < 3 and client_addr_retry_count < 3:
        needed = False

    return needed


def increment_retries(context, request, identifier):
    """
    Checks the amount of repeated request based on both the resource and
    the client addr. When an attacker spoofs the ip address the resource will
    still be protected against brute-forcing.
    """

    retry_count = _get_retry_count(context, identifier)
    client_addr_retry_count = _get_retry_count(context, request.client_addr)

    RedisSession().session.set("retry_count_{}_{}".format(context, identifier),
                               bytes([retry_count + 1]))
    RedisSession().session.set(
        "retry_count_{}_{}".format(context,  request.client_addr),
        bytes([client_addr_retry_count + 1]))


def invalidate_retry_count(context, request, identifier):
    RedisSession().session.delete(*(
        "retry_count_{}_{}".format(context, request.client_addr),
        "retry_count_{}_{}".format(context, identifier)))


def _get_retry_count(context, identifier):
    retry_count = 0
    cached_retry_count = RedisSession().session.get(
        "retry_count_{}_{}".format(context, identifier))

    if cached_retry_count:
        retry_count = int.from_bytes(cached_retry_count, 'big')

    return retry_count
