from django.contrib import admin
from .models import SmartCache


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
