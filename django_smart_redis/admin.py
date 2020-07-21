import redis

from .core.core import EzRedis
from .settings import redis_connect, namespace
from django.contrib import admin

from django_smart_redis.models import SmartCache


@admin.register(SmartCache)
class SmartCacheAdmin(admin.ModelAdmin):
    list_display = (
        'key',
    )
    readonly_fields = (
        'key',
        'value'
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


try:
    with EzRedis(**redis_connect) as r:
        print("Scan and delete cache...")
        for key in r.scan_iter(f"{namespace}:*"):
            print(f">>> Delete key '{key.decode()}'")
            r.delete(key)
            SmartCache._default_manager.all().delete()

except redis.exceptions.ConnectionError:
    print("!!! Cache not active !!!")
