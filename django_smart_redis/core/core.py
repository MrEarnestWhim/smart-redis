import json
import redis
import logging

from ..settings import redis_connect, namespace

logger = logging.getLogger(__name__)


class EzRedis(redis.StrictRedis):
    def __init__(self, *args, **kwargs):
        self.namespace = kwargs.pop('namespace') or ''
        super().__init__(*args, **kwargs)

    def __get_name(self, key):
        return f'{self.namespace}:{key}' if self.namespace else f'{key}'

    def ez_set_json(self, key: str, data) -> bool:
        return self.set(self.__get_name(key), json.dumps(data))

    def ez_set(self, key: str, data: dict) -> bool:
        return self.set(self.__get_name(key), data)

    def set(self, name, value, *args, **kwargs) -> bool:
        return super().set(self.__get_name(name), value, *args, **kwargs)

    def ez_get(self, key: str) -> str:
        return self.get(self.__get_name(key)).decode()

    def ez_get_json(self, key: str) -> dict:
        return json.loads(self.ez_get(key))

    def exists(self, key: str):
        return super().exists(self.__get_name(key))

    def ez_delete(self, key: str):
        return super().delete(self.__get_name(key))

    def get(self, key: str):
        return super().get(self.__get_name(key))


def clear_cache(key: (str, list, tuple)):
    def _clear(_key):
        try:
            with EzRedis(**redis_connect) as r:
                logger.debug(f"Delete cache '{_key}'")
                for __key in r.scan_iter(f"{namespace}:{_key}*"):
                    logger.debug(f">>> Delete key '{__key.decode()}'")
                    r.delete(__key)

        except redis.exceptions.ConnectionError as e:
            logger.error(e)

    if isinstance(key, (list, tuple)):
        for item in key:
            _clear(item)
    else:
        _clear(key)
