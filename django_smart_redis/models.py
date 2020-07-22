from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .core.core import clear_cache


class SmartCache(models.Model):
    key = models.TextField(verbose_name=_('Key'))
    value = models.TextField(verbose_name=_('Value'))
    content_type = models.TextField(verbose_name=_('Content Type'))

    class Meta:
        """Table information."""

        verbose_name = _('Saved cache')
        verbose_name_plural = _('Saved caches')

    def __str__(self):
        return self.key


@receiver(post_delete, sender=SmartCache)
def my_handler(sender, **kwargs):
    clear_cache(kwargs.get('instance').key)
