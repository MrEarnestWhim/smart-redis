from django.conf import settings

host = getattr(settings, 'SMART_REDIS_HOST', '127.0.0.1')
port = getattr(settings, 'SMART_REDIS_PORT', 6379)
db = getattr(settings, 'SMART_REDIS_DB', 0)
password = getattr(settings, 'SMART_REDIS_PASSWORD', None)
namespace = getattr(settings, 'SMART_REDIS_NAMESPACE', 'cache')

redis_connect = dict(
    host=host,
    port=port,
    db=db,
    password=password,
    namespace=namespace,
)
