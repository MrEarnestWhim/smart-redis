import redis
import logging

from django.apps import AppConfig

from .core.core import EzRedis
from .settings import redis_connect, namespace, auto_clear_cache

logger = logging.getLogger(__name__)


class DjangoSmartRedisConfig(AppConfig):
    name = 'django_smart_redis'
    verbose_name = "Smart Cache"

    def ready(self):
        if auto_clear_cache:
            from .models import SmartCache
            
            try:
                with EzRedis(**redis_connect) as r:
                    logger.debug("Scan and delete cache...")
                    for key in r.scan_iter(f"{namespace}:*"):
                        logger.debug(f">>> Delete key '{key.decode()}'")
                        r.delete(key)
                        SmartCache._default_manager.all().delete()

            except redis.exceptions.ConnectionError:
                logger.error("!!! Cache not active !!!")
