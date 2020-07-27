import functools
import logging

import redis
import hashlib
from django.http import HttpResponse
from django.template.response import ContentNotRenderedError

from .core import EzRedis
from ..models import SmartCache
from ..settings import redis_connect

logger = logging.getLogger(__name__)


def get_key_hash(key, qs_hash) -> str:
    if qs_hash:
        return key + ':' + qs_hash
    return key


def get_content_type(response) -> str:
    headers = getattr(response, '_headers', {})
    return headers.get('content-type')[1] if headers.get('content-type') else ''


def smart_cache(key):
    def decorate(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            qs_hash = ''
            qs = self.request.META.get('QUERY_STRING')
            if self.request.META.get('QUERY_STRING'):
                qs_hash = hashlib.sha512(qs.encode()).hexdigest()

            try:
                with EzRedis(**redis_connect) as r:
                    if int(r.exists(get_key_hash(key, qs_hash))):
                        return HttpResponse(
                            r.get(get_key_hash(key, qs_hash)),
                            content_type=r.get(key + ':content_type')
                        )

                    response = method(self, *args, **kwargs)

                    try:
                        content = response.content.decode()
                    except ContentNotRenderedError:
                        content = response.rendered_content

                    r.set(get_key_hash(key, qs_hash), content)
                    r.set(key + ':content_type', get_content_type(response))

                    SmartCache._default_manager.create(
                        key=get_key_hash(key, qs_hash),
                        value=content,
                        content_type=get_content_type(response),
                        qs=qs,
                    )

            except redis.exceptions.ConnectionError:
                logger.error("!!! Cache not active !!!")
                return method(self, *args, **kwargs)

            return response

        return wrapper

    return decorate
