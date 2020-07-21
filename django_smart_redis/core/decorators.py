import functools

import redis
import hashlib
from django.http import HttpResponse

from .core import EzRedis
from ..models import SmartCache
from ..settings import redis_connect


def get_key_hash(key, qs_hash):
    if qs_hash:
        return key + ':' + qs_hash
    return key


def out_cache(argument):
    def decorate(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            qs_hash = ''
            if self.request.META.get('QUERY_STRING'):
                qs_hash = hashlib.sha512(self.request.META.get('QUERY_STRING').encode()).hexdigest()

            try:
                with EzRedis(**redis_connect) as r:
                    key = argument
                    if int(r.exists(get_key_hash(key, qs_hash))):
                        return HttpResponse(r.get(get_key_hash(key, qs_hash)), content_type='application/json')

                    response = method(self, *args, **kwargs)
                    r.set(get_key_hash(key, qs_hash), response.content)

                    SmartCache._default_manager.create(
                        key=get_key_hash(key, qs_hash),
                        value=response.content.decode()
                    )

            except redis.exceptions.ConnectionError:
                return method(self, *args, **kwargs)

            return response

        return wrapper

    return decorate
