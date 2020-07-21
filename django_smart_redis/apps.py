import redis
import logging

from django.apps import AppConfig

from .core.core import EzRedis
from .models import SmartCache
from .settings import redis_connect, namespace

logger = logging.getLogger(__name__)


class DjangoSmartRedisConfig(AppConfig):
    name = 'django_smart_redis'
    verbose_name = "Smart Cache"

    def ready(self):
        try:
            with EzRedis(**redis_connect) as r:
                logger.debug("Scan and delete cache...")
                for key in r.scan_iter(f"{namespace}:*"):
                    logger.debug(f">>> Delete key '{key.decode()}'")
                    r.delete(key)
                    SmartCache._default_manager.all().delete()

        except redis.exceptions.ConnectionError:
            logger.error("!!! Cache not active !!!")
